import 'dart:async';
import 'package:geolocator/geolocator.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import '../../../core/constants/app_constants.dart';
import '../../../core/errors/app_errors.dart';
import '../../../core/utils/distance_utils.dart';
import '../models/checkpoint.dart';

typedef OnCheckpointArrived = void Function(String checkpointId);

class GeofenceService {
  final FlutterLocalNotificationsPlugin _notificationsPlugin;

  GeofenceService({FlutterLocalNotificationsPlugin? notificationsPlugin})
      : _notificationsPlugin =
            notificationsPlugin ?? FlutterLocalNotificationsPlugin();

  StreamSubscription<Position>? _positionSubscription;
  List<Checkpoint> _activeCheckpoints = [];
  OnCheckpointArrived? _onArrived;

  // Prevent duplicate triggers within a short window
  final Set<String> _recentlyTriggered = {};

  bool get isTracking => _positionSubscription != null;

  // ── Initialisation ────────────────────────────────────────────────────────

  Future<void> init() async {
    const android = AndroidInitializationSettings('@mipmap/ic_launcher');
    const darwin = DarwinInitializationSettings(
      requestAlertPermission: true,
      requestBadgePermission: true,
      requestSoundPermission: true,
    );
    const settings =
        InitializationSettings(android: android, iOS: darwin);
    await _notificationsPlugin.initialize(settings);

    // Create Android notification channel
    const channel = AndroidNotificationChannel(
      AppConstants.notifChannelId,
      AppConstants.notifChannelName,
      description: AppConstants.notifChannelDesc,
      importance: Importance.high,
      playSound: true,
    );
    await _notificationsPlugin
        .resolvePlatformSpecificImplementation<
            AndroidFlutterLocalNotificationsPlugin>()
        ?.createNotificationChannel(channel);
  }

  // ── Permission ────────────────────────────────────────────────────────────

  Future<void> requestPermissions() async {
    bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      throw const LocationPermissionException(
          'Location services are disabled. Enable them in device settings.');
    }

    LocationPermission permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        throw const LocationPermissionException(
            'Location permission denied by user.');
      }
    }
    if (permission == LocationPermission.deniedForever) {
      throw const LocationPermissionException(
          'Location permission permanently denied. Open app settings to grant it.');
    }
  }

  // ── Tracking ──────────────────────────────────────────────────────────────

  Future<void> startTracking({
    required List<Checkpoint> checkpoints,
    required OnCheckpointArrived onArrived,
  }) async {
    await requestPermissions();
    _activeCheckpoints = checkpoints;
    _onArrived = onArrived;
    _recentlyTriggered.clear();

    _positionSubscription?.cancel();
    _positionSubscription = Geolocator.getPositionStream(
      locationSettings: const LocationSettings(
        accuracy: LocationAccuracy.high,
        distanceFilter: AppConstants.locationDistanceFilterMeters,
      ),
    ).listen(_onPositionUpdate, onError: (_) {});
  }

  void updateCheckpoints(List<Checkpoint> checkpoints) {
    _activeCheckpoints = checkpoints;
    // Remove triggered IDs that are no longer in the list or are re-opened
    _recentlyTriggered.removeWhere(
      (id) => !checkpoints.any((c) => c.id == id && c.isCompleted),
    );
  }

  void stopTracking() {
    _positionSubscription?.cancel();
    _positionSubscription = null;
    _activeCheckpoints = [];
    _recentlyTriggered.clear();
  }

  // ── Internal ──────────────────────────────────────────────────────────────

  void _onPositionUpdate(Position position) {
    final pending = _activeCheckpoints
        .where((c) => !c.isCompleted && !_recentlyTriggered.contains(c.id))
        .toList();

    for (final checkpoint in pending) {
      final distance = DistanceUtils.haversine(
        position.latitude,
        position.longitude,
        checkpoint.latitude,
        checkpoint.longitude,
      );

      if (distance <= checkpoint.geofenceRadius) {
        _recentlyTriggered.add(checkpoint.id);
        _onArrived?.call(checkpoint.id);
        _showArrivalNotification(checkpoint);

        // Allow re-trigger only if manually unchecked (handled via updateCheckpoints)
        Future.delayed(const Duration(minutes: 2), () {
          _recentlyTriggered.remove(checkpoint.id);
        });
      }
    }
  }

  Future<void> _showArrivalNotification(Checkpoint checkpoint) async {
    const androidDetails = AndroidNotificationDetails(
      AppConstants.notifChannelId,
      AppConstants.notifChannelName,
      channelDescription: AppConstants.notifChannelDesc,
      importance: Importance.high,
      priority: Priority.high,
      icon: '@mipmap/ic_launcher',
    );
    const darwinDetails = DarwinNotificationDetails(
      presentAlert: true,
      presentSound: true,
    );
    const details =
        NotificationDetails(android: androidDetails, iOS: darwinDetails);

    await _notificationsPlugin.show(
      checkpoint.id.hashCode,
      '📍 Tappa raggiunta!',
      'Sei arrivato a ${checkpoint.name}',
      details,
    );
  }

  void dispose() {
    stopTracking();
  }
}
