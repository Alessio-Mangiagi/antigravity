class AppConstants {
  AppConstants._();

  // ── Google APIs ──────────────────────────────────────────────────────────
  // Replace with your key from https://console.cloud.google.com
  // Required APIs: Maps SDK Android/iOS, Directions API, Places API
  static const String googleMapsApiKey = 'YOUR_GOOGLE_MAPS_API_KEY';

  static const String directionsBaseUrl =
      'https://maps.googleapis.com/maps/api/directions/json';
  static const String placesAutocompleteUrl =
      'https://maps.googleapis.com/maps/api/place/autocomplete/json';
  static const String placesDetailsUrl =
      'https://maps.googleapis.com/maps/api/place/details/json';

  // ── Geofencing ────────────────────────────────────────────────────────────
  static const double defaultGeofenceRadiusMeters = 75.0;
  static const double minGeofenceRadiusMeters = 20.0;
  static const double maxGeofenceRadiusMeters = 500.0;

  // ── Location tracking ─────────────────────────────────────────────────────
  static const int locationDistanceFilterMeters = 10;

  // ── Hive boxes ────────────────────────────────────────────────────────────
  static const String checkpointsBox = 'checkpoints_box';
  static const String settingsBox = 'settings_box';

  // Settings keys
  static const String keyGeofenceRadius = 'geofence_radius';
  static const String keyRouteOrder = 'route_order'; // List<String> of ids

  // ── Notifications ─────────────────────────────────────────────────────────
  static const String notifChannelId = 'arrival_channel';
  static const String notifChannelName = 'Arrivo tappa';
  static const String notifChannelDesc =
      'Notifica automatica quando raggiungi una tappa';

  // ── Default map center (Rome) — overridden by user location ───────────────
  static const double defaultLat = 41.9028;
  static const double defaultLng = 12.4964;
  static const double defaultZoom = 13.0;
}
