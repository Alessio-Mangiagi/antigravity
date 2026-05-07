import 'package:hive/hive.dart';
import '../../route/models/place.dart';

part 'checkpoint_adapter.dart';

class Checkpoint {
  final String id;
  final String name;
  final String address;
  final double latitude;
  final double longitude;
  final bool isCompleted;
  final int orderIndex;
  final double geofenceRadius;
  final DateTime? completedAt;

  const Checkpoint({
    required this.id,
    required this.name,
    required this.address,
    required this.latitude,
    required this.longitude,
    this.isCompleted = false,
    required this.orderIndex,
    this.geofenceRadius = 75.0,
    this.completedAt,
  });

  factory Checkpoint.fromPlace(Place place, {int orderIndex = 0, double geofenceRadius = 75.0}) {
    return Checkpoint(
      id: place.id,
      name: place.name,
      address: place.address,
      latitude: place.latitude,
      longitude: place.longitude,
      orderIndex: orderIndex,
      geofenceRadius: geofenceRadius,
    );
  }

  Checkpoint copyWith({
    String? id,
    String? name,
    String? address,
    double? latitude,
    double? longitude,
    bool? isCompleted,
    int? orderIndex,
    double? geofenceRadius,
    DateTime? completedAt,
    bool clearCompletedAt = false,
  }) {
    return Checkpoint(
      id: id ?? this.id,
      name: name ?? this.name,
      address: address ?? this.address,
      latitude: latitude ?? this.latitude,
      longitude: longitude ?? this.longitude,
      isCompleted: isCompleted ?? this.isCompleted,
      orderIndex: orderIndex ?? this.orderIndex,
      geofenceRadius: geofenceRadius ?? this.geofenceRadius,
      completedAt: clearCompletedAt ? null : (completedAt ?? this.completedAt),
    );
  }

  Place toPlace() => Place(
        id: id,
        name: name,
        address: address,
        latitude: latitude,
        longitude: longitude,
      );

  Map<String, dynamic> toJson() => {
        'id': id,
        'name': name,
        'address': address,
        'latitude': latitude,
        'longitude': longitude,
        'isCompleted': isCompleted,
        'orderIndex': orderIndex,
        'geofenceRadius': geofenceRadius,
        'completedAt': completedAt?.toIso8601String(),
      };

  factory Checkpoint.fromJson(Map<String, dynamic> json) => Checkpoint(
        id: json['id'] as String,
        name: json['name'] as String,
        address: json['address'] as String,
        latitude: (json['latitude'] as num).toDouble(),
        longitude: (json['longitude'] as num).toDouble(),
        isCompleted: json['isCompleted'] as bool? ?? false,
        orderIndex: json['orderIndex'] as int? ?? 0,
        geofenceRadius: (json['geofenceRadius'] as num?)?.toDouble() ?? 75.0,
        completedAt: json['completedAt'] != null
            ? DateTime.tryParse(json['completedAt'] as String)
            : null,
      );

  @override
  bool operator ==(Object other) =>
      identical(this, other) || other is Checkpoint && other.id == id;

  @override
  int get hashCode => id.hashCode;

  @override
  String toString() => 'Checkpoint(id: $id, name: $name, order: $orderIndex, done: $isCompleted)';
}
