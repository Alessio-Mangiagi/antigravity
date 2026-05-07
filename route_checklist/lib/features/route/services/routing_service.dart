import 'dart:convert';
import 'package:http/http.dart' as http;
import '../../../core/constants/app_constants.dart';
import '../../../core/errors/app_errors.dart';
import '../../../core/utils/distance_utils.dart';
import '../../checklist/models/checkpoint.dart';
import '../models/place.dart';
import '../models/route_result.dart';

class RoutingService {
  final http.Client _client;

  RoutingService({http.Client? client}) : _client = client ?? http.Client();

  // ── Places Autocomplete ────────────────────────────────────────────────────

  Future<List<PlaceSuggestion>> autocomplete(String query) async {
    if (query.trim().length < 2) return [];

    final uri = Uri.parse(AppConstants.placesAutocompleteUrl).replace(
      queryParameters: {
        'input': query,
        'key': AppConstants.googleMapsApiKey,
        'language': 'it',
        'types': 'geocode|establishment',
      },
    );

    try {
      final response = await _client.get(uri).timeout(const Duration(seconds: 8));
      if (response.statusCode != 200) return [];

      final data = json.decode(response.body) as Map<String, dynamic>;
      final status = data['status'] as String;
      if (status == 'ZERO_RESULTS') return [];
      if (status != 'OK') {
        throw PlacesException('Autocomplete API error: $status');
      }

      final predictions = data['predictions'] as List<dynamic>;
      return predictions
          .map((p) => PlaceSuggestion.fromJson(p as Map<String, dynamic>))
          .toList();
    } on PlacesException {
      rethrow;
    } catch (e) {
      throw PlacesException('Autocomplete request failed: $e');
    }
  }

  Future<Place?> fetchPlaceDetails(String placeId, String uuid) async {
    final uri = Uri.parse(AppConstants.placesDetailsUrl).replace(
      queryParameters: {
        'place_id': placeId,
        'fields': 'name,formatted_address,geometry',
        'key': AppConstants.googleMapsApiKey,
        'language': 'it',
      },
    );

    try {
      final response = await _client.get(uri).timeout(const Duration(seconds: 8));
      if (response.statusCode != 200) return null;

      final data = json.decode(response.body) as Map<String, dynamic>;
      final status = data['status'] as String;
      if (status != 'OK') {
        throw PlacesException('Place Details API error: $status');
      }

      final result = data['result'] as Map<String, dynamic>;
      final geometry = result['geometry'] as Map<String, dynamic>;
      final location = geometry['location'] as Map<String, dynamic>;

      return Place(
        id: uuid,
        name: result['name'] as String,
        address: result['formatted_address'] as String,
        latitude: (location['lat'] as num).toDouble(),
        longitude: (location['lng'] as num).toDouble(),
      );
    } on PlacesException {
      rethrow;
    } catch (e) {
      throw PlacesException('Place details request failed: $e');
    }
  }

  // ── Route Optimisation ─────────────────────────────────────────────────────

  /// Calculates an optimised route between [checkpoints].
  /// Tries Google Directions API first; falls back to nearest-neighbour on failure.
  Future<RouteResult> optimizeRoute(List<Checkpoint> checkpoints) async {
    if (checkpoints.isEmpty) {
      return RouteResult(
        orderedCheckpoints: [],
        polylinePoints: [],
        totalDistanceMeters: 0,
        totalDurationSeconds: 0,
        isApiOptimized: false,
      );
    }
    if (checkpoints.length == 1) {
      return RouteResult(
        orderedCheckpoints: checkpoints,
        polylinePoints: [
          (checkpoints.first.latitude, checkpoints.first.longitude)
        ],
        totalDistanceMeters: 0,
        totalDurationSeconds: 0,
        isApiOptimized: false,
      );
    }

    try {
      return await _optimizeWithApi(checkpoints);
    } catch (_) {
      return _optimizeLocally(checkpoints);
    }
  }

  Future<RouteResult> _optimizeWithApi(List<Checkpoint> checkpoints) async {
    final origin = checkpoints.first;
    final destination = checkpoints.last;
    final waypoints = checkpoints.sublist(1, checkpoints.length - 1);

    final waypointStr = waypoints
        .map((c) => '${c.latitude},${c.longitude}')
        .join('|');

    final queryParams = <String, String>{
      'origin': '${origin.latitude},${origin.longitude}',
      'destination': '${destination.latitude},${destination.longitude}',
      'key': AppConstants.googleMapsApiKey,
      'optimize': 'true',
      'mode': 'driving',
      'language': 'it',
    };

    if (waypointStr.isNotEmpty) {
      queryParams['waypoints'] = 'optimize:true|$waypointStr';
    }

    final uri = Uri.parse(AppConstants.directionsBaseUrl)
        .replace(queryParameters: queryParams);

    final response = await _client.get(uri).timeout(const Duration(seconds: 12));

    if (response.statusCode != 200) {
      throw RoutingException(
          'Directions API HTTP ${response.statusCode}');
    }

    final data = json.decode(response.body) as Map<String, dynamic>;
    final status = data['status'] as String;

    if (status == 'NOT_FOUND' || status == 'ZERO_RESULTS') {
      throw RoutingException('No route found', apiStatus: status);
    }
    if (status != 'OK') {
      throw RoutingException('Directions API error', apiStatus: status);
    }

    final routes = data['routes'] as List<dynamic>;
    final route = routes.first as Map<String, dynamic>;

    // Optimised waypoint order (indices into original waypoints list, excluding origin/dest)
    final rawOrder =
        (route['waypoint_order'] as List<dynamic>?)?.cast<int>() ?? [];

    // Rebuild checkpoint order: origin → (reordered waypoints) → destination
    final reorderedMiddle = rawOrder.map((i) => waypoints[i]).toList();
    final orderedCheckpoints = [origin, ...reorderedMiddle, destination];

    // Re-assign orderIndex
    final indexed = orderedCheckpoints
        .asMap()
        .entries
        .map((e) => e.value.copyWith(orderIndex: e.key))
        .toList();

    // Decode overview polyline
    final overviewPolyline =
        route['overview_polyline']['points'] as String? ?? '';
    final polylinePoints = DistanceUtils.decodePolyline(overviewPolyline);

    // Sum distance and duration from legs
    final legs = route['legs'] as List<dynamic>;
    int totalDistance = 0;
    int totalDuration = 0;
    for (final leg in legs) {
      totalDistance +=
          ((leg as Map<String, dynamic>)['distance']['value'] as int);
      totalDuration += (leg['duration']['value'] as int);
    }

    return RouteResult(
      orderedCheckpoints: indexed,
      polylinePoints: polylinePoints,
      totalDistanceMeters: totalDistance,
      totalDurationSeconds: totalDuration,
      isApiOptimized: true,
    );
  }

  RouteResult _optimizeLocally(List<Checkpoint> checkpoints) {
    final points =
        checkpoints.map((c) => (c.latitude, c.longitude)).toList();
    final order = DistanceUtils.nearestNeighbourOrder(points);
    final ordered = order.asMap().entries
        .map((e) => checkpoints[e.value].copyWith(orderIndex: e.key))
        .toList();

    // Approximate distance using haversine between consecutive stops
    double totalDist = 0;
    for (int i = 0; i < ordered.length - 1; i++) {
      totalDist += DistanceUtils.haversine(
        ordered[i].latitude,
        ordered[i].longitude,
        ordered[i + 1].latitude,
        ordered[i + 1].longitude,
      );
    }

    // Straight-line polyline (no road snapping in fallback)
    final polyline = ordered.map((c) => (c.latitude, c.longitude)).toList();

    return RouteResult(
      orderedCheckpoints: ordered,
      polylinePoints: polyline,
      totalDistanceMeters: totalDist.round(),
      totalDurationSeconds: (totalDist / 10).round(), // rough ~36 km/h estimate
      isApiOptimized: false,
    );
  }
}
