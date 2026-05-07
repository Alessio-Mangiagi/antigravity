import 'dart:math';

class DistanceUtils {
  DistanceUtils._();

  static const double _earthRadiusMeters = 6371000.0;

  /// Haversine formula — returns distance in meters between two coordinates.
  static double haversine(
    double lat1,
    double lon1,
    double lat2,
    double lon2,
  ) {
    final dLat = _toRad(lat2 - lat1);
    final dLon = _toRad(lon2 - lon1);

    final a = sin(dLat / 2) * sin(dLat / 2) +
        cos(_toRad(lat1)) * cos(_toRad(lat2)) * sin(dLon / 2) * sin(dLon / 2);

    final c = 2 * atan2(sqrt(a), sqrt(1 - a));
    return _earthRadiusMeters * c;
  }

  static double _toRad(double deg) => deg * pi / 180.0;

  /// Human-readable distance string (e.g. "350 m" or "2.4 km").
  static String formatDistance(double meters) {
    if (meters < 1000) {
      return '${meters.round()} m';
    }
    return '${(meters / 1000).toStringAsFixed(1)} km';
  }

  /// Human-readable duration string from seconds.
  static String formatDuration(int seconds) {
    if (seconds < 60) return '< 1 min';
    final minutes = seconds ~/ 60;
    if (minutes < 60) return '$minutes min';
    final hours = minutes ~/ 60;
    final remainingMin = minutes % 60;
    if (remainingMin == 0) return '${hours}h';
    return '${hours}h ${remainingMin}min';
  }

  /// Nearest-neighbour TSP approximation.
  /// Returns indices into [points] in visitation order.
  /// Complexity O(n²) — fine up to ~50 waypoints.
  static List<int> nearestNeighbourOrder(List<(double, double)> points) {
    if (points.isEmpty) return [];
    if (points.length == 1) return [0];

    final visited = List.filled(points.length, false);
    final order = <int>[0];
    visited[0] = true;

    while (order.length < points.length) {
      final current = order.last;
      double minDist = double.infinity;
      int nextIndex = -1;

      for (int i = 0; i < points.length; i++) {
        if (visited[i]) continue;
        final d = haversine(
          points[current].$1,
          points[current].$2,
          points[i].$1,
          points[i].$2,
        );
        if (d < minDist) {
          minDist = d;
          nextIndex = i;
        }
      }

      visited[nextIndex] = true;
      order.add(nextIndex);
    }
    return order;
  }

  /// Decode a Google-encoded polyline string into a list of [lat, lng] pairs.
  static List<(double, double)> decodePolyline(String encoded) {
    final result = <(double, double)>[];
    int index = 0;
    final len = encoded.length;
    int lat = 0, lng = 0;

    while (index < len) {
      int b, shift = 0, r = 0;
      do {
        b = encoded.codeUnitAt(index++) - 63;
        r |= (b & 0x1f) << shift;
        shift += 5;
      } while (b >= 0x20);
      final dLat = ((r & 1) != 0 ? ~(r >> 1) : (r >> 1));
      lat += dLat;

      shift = 0;
      r = 0;
      do {
        b = encoded.codeUnitAt(index++) - 63;
        r |= (b & 0x1f) << shift;
        shift += 5;
      } while (b >= 0x20);
      final dLng = ((r & 1) != 0 ? ~(r >> 1) : (r >> 1));
      lng += dLng;

      result.add((lat / 1e5, lng / 1e5));
    }
    return result;
  }
}
