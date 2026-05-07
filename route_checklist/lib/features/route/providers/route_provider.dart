import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/route_result.dart';
import '../services/routing_service.dart';
import '../../checklist/models/checkpoint.dart';
import '../../checklist/providers/checklist_provider.dart';

// ── Service provider ──────────────────────────────────────────────────────────

final routingServiceProvider = Provider<RoutingService>((ref) {
  return RoutingService();
});

// ── State ─────────────────────────────────────────────────────────────────────

class RouteState {
  final RouteResult? result;
  final bool isCalculating;
  final String? error;

  const RouteState({
    this.result,
    this.isCalculating = false,
    this.error,
  });

  RouteState copyWith({
    RouteResult? result,
    bool? isCalculating,
    String? error,
    bool clearError = false,
    bool clearResult = false,
  }) {
    return RouteState(
      result: clearResult ? null : (result ?? this.result),
      isCalculating: isCalculating ?? this.isCalculating,
      error: clearError ? null : (error ?? this.error),
    );
  }

  bool get hasRoute => result != null;
}

// ── Notifier ──────────────────────────────────────────────────────────────────

class RouteNotifier extends StateNotifier<RouteState> {
  final RoutingService _routingService;
  final Ref _ref;

  RouteNotifier(this._routingService, this._ref) : super(const RouteState());

  Future<void> calculateRoute(List<Checkpoint> checkpoints) async {
    if (checkpoints.length < 2) {
      state = state.copyWith(
          error: 'Aggiungi almeno 2 tappe per calcolare il percorso.',
          clearResult: true);
      return;
    }

    state = state.copyWith(isCalculating: true, clearError: true);

    try {
      final result = await _routingService.optimizeRoute(checkpoints);

      // Push the optimised order back to checklist
      await _ref
          .read(checklistProvider.notifier)
          .applyOptimisedOrder(result.orderedCheckpoints);

      state = state.copyWith(result: result, isCalculating: false);
    } catch (e) {
      state = state.copyWith(
        isCalculating: false,
        error: 'Errore calcolo percorso: $e',
      );
    }
  }

  void clearRoute() {
    state = const RouteState();
  }

  void clearError() => state = state.copyWith(clearError: true);
}

// ── Provider ──────────────────────────────────────────────────────────────────

final routeProvider =
    StateNotifierProvider<RouteNotifier, RouteState>((ref) {
  final routing = ref.watch(routingServiceProvider);
  return RouteNotifier(routing, ref);
});
