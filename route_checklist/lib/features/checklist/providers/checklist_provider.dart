import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/constants/app_constants.dart';
import '../models/checkpoint.dart';
import '../services/geofence_service.dart';
import '../services/storage_service.dart';
import '../../route/models/place.dart';

// ── Service Providers ─────────────────────────────────────────────────────────

final storageServiceProvider = Provider<StorageService>((ref) {
  return StorageService();
});

final geofenceServiceProvider = Provider<GeofenceService>((ref) {
  final service = GeofenceService();
  ref.onDispose(service.dispose);
  return service;
});

// ── State ─────────────────────────────────────────────────────────────────────

class ChecklistState {
  final List<Checkpoint> checkpoints;
  final bool isLoading;
  final String? error;
  final double geofenceRadius;
  final bool isTrackingActive;

  const ChecklistState({
    this.checkpoints = const [],
    this.isLoading = false,
    this.error,
    this.geofenceRadius = AppConstants.defaultGeofenceRadiusMeters,
    this.isTrackingActive = false,
  });

  ChecklistState copyWith({
    List<Checkpoint>? checkpoints,
    bool? isLoading,
    String? error,
    double? geofenceRadius,
    bool? isTrackingActive,
    bool clearError = false,
  }) {
    return ChecklistState(
      checkpoints: checkpoints ?? this.checkpoints,
      isLoading: isLoading ?? this.isLoading,
      error: clearError ? null : (error ?? this.error),
      geofenceRadius: geofenceRadius ?? this.geofenceRadius,
      isTrackingActive: isTrackingActive ?? this.isTrackingActive,
    );
  }

  bool get isEmpty => checkpoints.isEmpty;
  bool get allCompleted =>
      checkpoints.isNotEmpty && checkpoints.every((c) => c.isCompleted);
  int get completedCount => checkpoints.where((c) => c.isCompleted).length;

  /// Returns the first uncompleted checkpoint in order, or null if all done.
  Checkpoint? get nextTarget {
    final pending =
        checkpoints.where((c) => !c.isCompleted).toList();
    if (pending.isEmpty) return null;
    pending.sort((a, b) => a.orderIndex.compareTo(b.orderIndex));
    return pending.first;
  }
}

// ── Notifier ──────────────────────────────────────────────────────────────────

class ChecklistNotifier extends StateNotifier<ChecklistState> {
  final StorageService _storage;
  final GeofenceService _geofence;

  ChecklistNotifier(this._storage, this._geofence)
      : super(const ChecklistState()) {
    _load();
  }

  // ── Init ────────────────────────────────────────────────────────────────────

  Future<void> _load() async {
    state = state.copyWith(isLoading: true, clearError: true);
    try {
      await _storage.init();
      final checkpoints = _storage.loadCheckpoints();
      final radius = _storage.loadGeofenceRadius();
      state = state.copyWith(
        checkpoints: checkpoints,
        geofenceRadius: radius,
        isLoading: false,
      );
    } catch (e) {
      state = state.copyWith(isLoading: false, error: e.toString());
    }
  }

  // ── Checkpoint management ─────────────────────────────────────────────────

  Future<void> addCheckpoint(Place place) async {
    final orderIndex = state.checkpoints.length;
    final checkpoint = Checkpoint.fromPlace(
      place,
      orderIndex: orderIndex,
      geofenceRadius: state.geofenceRadius,
    );

    final updated = [...state.checkpoints, checkpoint];
    state = state.copyWith(checkpoints: updated);

    try {
      await _storage.saveCheckpoint(checkpoint);
      _syncGeofence();
    } catch (e) {
      // Rollback
      state = state.copyWith(
        checkpoints: state.checkpoints.where((c) => c.id != checkpoint.id).toList(),
        error: 'Errore salvataggio: $e',
      );
    }
  }

  Future<void> removeCheckpoint(String id) async {
    final prev = state.checkpoints;
    final updated = prev.where((c) => c.id != id).toList();

    // Re-index order
    final reindexed = updated
        .asMap()
        .entries
        .map((e) => e.value.copyWith(orderIndex: e.key))
        .toList();

    state = state.copyWith(checkpoints: reindexed);

    try {
      await _storage.deleteCheckpoint(id);
      await _storage.saveAllCheckpoints(reindexed);
      _syncGeofence();
    } catch (e) {
      state = state.copyWith(checkpoints: prev, error: 'Errore rimozione: $e');
    }
  }

  Future<void> toggleCheckpoint(String id) async {
    final prev = state.checkpoints;
    final updated = prev.map((c) {
      if (c.id != id) return c;
      final nowCompleted = !c.isCompleted;
      return c.copyWith(
        isCompleted: nowCompleted,
        completedAt: nowCompleted ? DateTime.now() : null,
        clearCompletedAt: !nowCompleted,
      );
    }).toList();

    state = state.copyWith(checkpoints: updated);

    try {
      final changed = updated.firstWhere((c) => c.id == id);
      await _storage.saveCheckpoint(changed);
      _syncGeofence();
    } catch (e) {
      state = state.copyWith(checkpoints: prev, error: 'Errore aggiornamento: $e');
    }
  }

  /// Called automatically by GeofenceService when user enters a waypoint radius.
  Future<void> autoCompleteCheckpoint(String id) async {
    final already = state.checkpoints.any((c) => c.id == id && c.isCompleted);
    if (already) return;
    await toggleCheckpoint(id);
  }

  Future<void> reorderCheckpoints(int oldIndex, int newIndex) async {
    final list = [...state.checkpoints];
    if (newIndex > oldIndex) newIndex--;
    final item = list.removeAt(oldIndex);
    list.insert(newIndex, item);

    final reindexed = list
        .asMap()
        .entries
        .map((e) => e.value.copyWith(orderIndex: e.key))
        .toList();

    state = state.copyWith(checkpoints: reindexed);

    try {
      await _storage.saveAllCheckpoints(reindexed);
      _syncGeofence();
    } catch (e) {
      state = state.copyWith(error: 'Errore riordino: $e');
    }
  }

  /// Replace entire checkpoint list (called after route optimisation).
  Future<void> applyOptimisedOrder(List<Checkpoint> ordered) async {
    state = state.copyWith(checkpoints: ordered);
    try {
      await _storage.saveAllCheckpoints(ordered);
      _syncGeofence();
    } catch (e) {
      state = state.copyWith(error: 'Errore salvataggio ordine: $e');
    }
  }

  Future<void> resetAllCheckpoints() async {
    final reset = state.checkpoints
        .map((c) => c.copyWith(
              isCompleted: false,
              clearCompletedAt: true,
            ))
        .toList();
    state = state.copyWith(checkpoints: reset);
    await _storage.saveAllCheckpoints(reset);
    _syncGeofence();
  }

  // ── Settings ───────────────────────────────────────────────────────────────

  Future<void> setGeofenceRadius(double radius) async {
    final clamped = radius.clamp(
      AppConstants.minGeofenceRadiusMeters,
      AppConstants.maxGeofenceRadiusMeters,
    );
    state = state.copyWith(geofenceRadius: clamped);
    await _storage.saveGeofenceRadius(clamped);

    // Update radius on all non-completed checkpoints
    final updated = state.checkpoints
        .map((c) => c.isCompleted ? c : c.copyWith(geofenceRadius: clamped))
        .toList();
    state = state.copyWith(checkpoints: updated);
    await _storage.saveAllCheckpoints(updated);
    _syncGeofence();
  }

  // ── Geofence tracking ──────────────────────────────────────────────────────

  Future<void> startTracking() async {
    state = state.copyWith(clearError: true);
    try {
      await _geofence.init();
      await _geofence.startTracking(
        checkpoints: state.checkpoints,
        onArrived: (id) => autoCompleteCheckpoint(id),
      );
      state = state.copyWith(isTrackingActive: true);
    } catch (e) {
      state = state.copyWith(error: e.toString());
    }
  }

  void stopTracking() {
    _geofence.stopTracking();
    state = state.copyWith(isTrackingActive: false);
  }

  void _syncGeofence() {
    if (state.isTrackingActive) {
      _geofence.updateCheckpoints(state.checkpoints);
    }
  }

  void clearError() => state = state.copyWith(clearError: true);
}

// ── Provider ──────────────────────────────────────────────────────────────────

final checklistProvider =
    StateNotifierProvider<ChecklistNotifier, ChecklistState>((ref) {
  final storage = ref.watch(storageServiceProvider);
  final geofence = ref.watch(geofenceServiceProvider);
  return ChecklistNotifier(storage, geofence);
});
