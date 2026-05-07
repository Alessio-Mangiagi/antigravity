/// Thrown when the routing API returns an error or non-OK status.
class RoutingException implements Exception {
  final String message;
  final String? apiStatus;
  const RoutingException(this.message, {this.apiStatus});

  @override
  String toString() => 'RoutingException: $message (status: $apiStatus)';
}

/// Thrown when the Places API returns an error.
class PlacesException implements Exception {
  final String message;
  const PlacesException(this.message);

  @override
  String toString() => 'PlacesException: $message';
}

/// Thrown when GPS permission is denied.
class LocationPermissionException implements Exception {
  final String message;
  const LocationPermissionException(this.message);

  @override
  String toString() => 'LocationPermissionException: $message';
}

/// Thrown when Hive storage operation fails.
class StorageException implements Exception {
  final String message;
  const StorageException(this.message);

  @override
  String toString() => 'StorageException: $message';
}
