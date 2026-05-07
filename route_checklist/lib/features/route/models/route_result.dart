import '../../checklist/models/checkpoint.dart';

class RouteResult {
  /// Checkpoints in the optimised visitation order.
  final List<Checkpoint> orderedCheckpoints;

  /// Decoded lat/lng pairs for the full polyline.
  final List<(double lat, double lng)> polylinePoints;

  /// Total road distance in metres.
  final int totalDistanceMeters;

  /// Total estimated travel time in seconds.
  final int totalDurationSeconds;

  /// Whether the order was produced by the Google API (true) or the
  /// local nearest-neighbour fallback (false).
  final bool isApiOptimized;

  const RouteResult({
    required this.orderedCheckpoints,
    required this.polylinePoints,
    required this.totalDistanceMeters,
    required this.totalDurationSeconds,
    required this.isApiOptimized,
  });

  RouteResult copyWith({
    List<Checkpoint>? orderedCheckpoints,
    List<(double, double)>? polylinePoints,
    int? totalDistanceMeters,
    int? totalDurationSeconds,
    bool? isApiOptimized,
  }) {
    return RouteResult(
      orderedCheckpoints: orderedCheckpoints ?? this.orderedCheckpoints,
      polylinePoints: polylinePoints ?? this.polylinePoints,
      totalDistanceMeters: totalDistanceMeters ?? this.totalDistanceMeters,
      totalDurationSeconds: totalDurationSeconds ?? this.totalDurationSeconds,
      isApiOptimized: isApiOptimized ?? this.isApiOptimized,
    );
  }
}
