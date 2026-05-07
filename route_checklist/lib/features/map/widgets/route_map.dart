import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:geolocator/geolocator.dart';
import '../../../core/constants/app_constants.dart';
import '../../checklist/models/checkpoint.dart';
import '../../checklist/providers/checklist_provider.dart';
import '../../route/providers/route_provider.dart';

class RouteMap extends ConsumerStatefulWidget {
  const RouteMap({super.key});

  @override
  // ignore: library_private_types_in_public_api
  RouteMapState createState() => RouteMapState();
}

/// State is public so [MainScreen] can hold a [GlobalKey<RouteMapState>]
/// and call [moveTo] to animate the camera.
class RouteMapState extends ConsumerState<RouteMap> {
  final Completer<GoogleMapController> _controllerCompleter = Completer();
  GoogleMapController? _mapController;
  LatLng _center =
      const LatLng(AppConstants.defaultLat, AppConstants.defaultLng);

  @override
  void initState() {
    super.initState();
    _initUserLocation();
  }

  @override
  void dispose() {
    _mapController?.dispose();
    super.dispose();
  }

  Future<void> _initUserLocation() async {
    try {
      final permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied ||
          permission == LocationPermission.deniedForever) return;

      final pos = await Geolocator.getCurrentPosition(
        locationSettings:
            const LocationSettings(accuracy: LocationAccuracy.high),
      );
      final userLatLng = LatLng(pos.latitude, pos.longitude);
      if (mounted) {
        setState(() => _center = userLatLng);
        _mapController?.animateCamera(
          CameraUpdate.newLatLngZoom(userLatLng, AppConstants.defaultZoom),
        );
      }
    } catch (_) {}
  }

  /// Animate camera to [target] at zoom 16.
  Future<void> moveTo(LatLng target) async {
    final controller = await _controllerCompleter.future;
    controller.animateCamera(
      CameraUpdate.newLatLngZoom(target, 16.0),
    );
  }

  @override
  Widget build(BuildContext context) {
    final checklistState = ref.watch(checklistProvider);
    final routeState = ref.watch(routeProvider);

    final markers = _buildMarkers(
      checkpoints: checklistState.checkpoints,
      nextTargetId: checklistState.nextTarget?.id,
    );

    final polylines = _buildPolylines(routeState);

    return GoogleMap(
      onMapCreated: (controller) {
        if (!_controllerCompleter.isCompleted) {
          _controllerCompleter.complete(controller);
        }
        _mapController = controller;
        _fitBounds(checklistState.checkpoints);
      },
      initialCameraPosition: CameraPosition(
        target: _center,
        zoom: AppConstants.defaultZoom,
      ),
      markers: markers,
      polylines: polylines,
      myLocationEnabled: true,
      myLocationButtonEnabled: false,
      zoomControlsEnabled: false,
      mapToolbarEnabled: false,
      compassEnabled: true,
      mapType: MapType.normal,
    );
  }

  // ── Markers ────────────────────────────────────────────────────────────────

  Set<Marker> _buildMarkers({
    required List<Checkpoint> checkpoints,
    required String? nextTargetId,
  }) {
    final markers = <Marker>{};
    final sorted = [...checkpoints]
      ..sort((a, b) => a.orderIndex.compareTo(b.orderIndex));

    for (int i = 0; i < sorted.length; i++) {
      final checkpoint = sorted[i];
      final isFirst = i == 0;
      final isLast = i == sorted.length - 1;
      final isNext = checkpoint.id == nextTargetId;

      final hue = _markerHue(
        isCompleted: checkpoint.isCompleted,
        isFirst: isFirst,
        isLast: isLast,
        isNext: isNext,
      );

      markers.add(
        Marker(
          markerId: MarkerId(checkpoint.id),
          position: LatLng(checkpoint.latitude, checkpoint.longitude),
          icon: BitmapDescriptor.defaultMarkerWithHue(hue),
          infoWindow: InfoWindow(
            title: '${i + 1}. ${checkpoint.name}',
            snippet: checkpoint.isCompleted
                ? '✅ Completata'
                : isNext
                    ? '🎯 Prossima tappa'
                    : checkpoint.address,
          ),
          zIndex: isNext ? 2.0 : (isFirst || isLast ? 1.5 : 1.0),
        ),
      );
    }
    return markers;
  }

  double _markerHue({
    required bool isCompleted,
    required bool isFirst,
    required bool isLast,
    required bool isNext,
  }) {
    if (isCompleted) return BitmapDescriptor.hueGreen;
    if (isNext) return BitmapDescriptor.hueOrange;
    if (isFirst) return BitmapDescriptor.hueAzure;
    if (isLast) return BitmapDescriptor.hueViolet;
    return BitmapDescriptor.hueRed;
  }

  // ── Polylines ──────────────────────────────────────────────────────────────

  Set<Polyline> _buildPolylines(RouteState routeState) {
    if (routeState.result == null) return {};
    final points = routeState.result!.polylinePoints
        .map((p) => LatLng(p.$1, p.$2))
        .toList();
    if (points.isEmpty) return {};

    return {
      Polyline(
        polylineId: const PolylineId('route'),
        points: points,
        color: const Color(0xFF1976D2),
        width: 5,
        jointType: JointType.round,
        startCap: Cap.roundCap,
        endCap: Cap.roundCap,
        geodesic: true,
      ),
    };
  }

  // ── Camera fit ─────────────────────────────────────────────────────────────

  void _fitBounds(List<Checkpoint> checkpoints) {
    if (checkpoints.isEmpty || _mapController == null) return;

    double minLat = checkpoints.first.latitude;
    double maxLat = checkpoints.first.latitude;
    double minLng = checkpoints.first.longitude;
    double maxLng = checkpoints.first.longitude;

    for (final c in checkpoints) {
      if (c.latitude < minLat) minLat = c.latitude;
      if (c.latitude > maxLat) maxLat = c.latitude;
      if (c.longitude < minLng) minLng = c.longitude;
      if (c.longitude > maxLng) maxLng = c.longitude;
    }

    _mapController!.animateCamera(
      CameraUpdate.newLatLngBounds(
        LatLngBounds(
          southwest: LatLng(minLat - 0.01, minLng - 0.01),
          northeast: LatLng(maxLat + 0.01, maxLng + 0.01),
        ),
        80.0,
      ),
    );
  }
}
