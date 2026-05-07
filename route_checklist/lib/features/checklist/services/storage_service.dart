import 'package:hive_flutter/hive_flutter.dart';
import '../../../core/constants/app_constants.dart';
import '../../../core/errors/app_errors.dart';
import '../models/checkpoint.dart';

class StorageService {
  late Box<Checkpoint> _checkpointsBox;
  late Box<dynamic> _settingsBox;
  bool _initialized = false;

  Future<void> init() async {
    if (_initialized) return;
    _checkpointsBox = Hive.box<Checkpoint>(AppConstants.checkpointsBox);
    _settingsBox = Hive.box<dynamic>(AppConstants.settingsBox);
    _initialized = true;
  }

  // ── Checkpoint CRUD ────────────────────────────────────────────────────────

  List<Checkpoint> loadCheckpoints() {
    _assertInitialized();
    final all = _checkpointsBox.values.toList();
    all.sort((a, b) => a.orderIndex.compareTo(b.orderIndex));
    return all;
  }

  Future<void> saveCheckpoint(Checkpoint checkpoint) async {
    _assertInitialized();
    try {
      await _checkpointsBox.put(checkpoint.id, checkpoint);
    } catch (e) {
      throw StorageException('Failed to save checkpoint: $e');
    }
  }

  Future<void> saveAllCheckpoints(List<Checkpoint> checkpoints) async {
    _assertInitialized();
    try {
      final map = {for (final c in checkpoints) c.id: c};
      await _checkpointsBox.putAll(map);
    } catch (e) {
      throw StorageException('Failed to save checkpoints: $e');
    }
  }

  Future<void> deleteCheckpoint(String id) async {
    _assertInitialized();
    try {
      await _checkpointsBox.delete(id);
    } catch (e) {
      throw StorageException('Failed to delete checkpoint: $e');
    }
  }

  Future<void> clearCheckpoints() async {
    _assertInitialized();
    await _checkpointsBox.clear();
  }

  // ── Settings ───────────────────────────────────────────────────────────────

  double loadGeofenceRadius() {
    _assertInitialized();
    return (_settingsBox.get(AppConstants.keyGeofenceRadius) as num?)
            ?.toDouble() ??
        AppConstants.defaultGeofenceRadiusMeters;
  }

  Future<void> saveGeofenceRadius(double radius) async {
    _assertInitialized();
    await _settingsBox.put(AppConstants.keyGeofenceRadius, radius);
  }

  // ── Private ────────────────────────────────────────────────────────────────

  void _assertInitialized() {
    if (!_initialized) {
      throw StorageException(
          'StorageService not initialized. Call init() first.');
    }
  }
}
