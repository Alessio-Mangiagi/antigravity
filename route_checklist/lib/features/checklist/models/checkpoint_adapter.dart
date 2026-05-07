part of 'checkpoint.dart';

// typeId = 1
class CheckpointAdapter extends TypeAdapter<Checkpoint> {
  @override
  final int typeId = 1;

  @override
  Checkpoint read(BinaryReader reader) {
    final id = reader.read() as String;
    final name = reader.read() as String;
    final address = reader.read() as String;
    final latitude = reader.read() as double;
    final longitude = reader.read() as double;
    final isCompleted = reader.read() as bool;
    final orderIndex = reader.read() as int;
    final geofenceRadius = reader.read() as double;
    final completedAtRaw = reader.read();
    final completedAt = completedAtRaw != null
        ? DateTime.tryParse(completedAtRaw as String)
        : null;

    return Checkpoint(
      id: id,
      name: name,
      address: address,
      latitude: latitude,
      longitude: longitude,
      isCompleted: isCompleted,
      orderIndex: orderIndex,
      geofenceRadius: geofenceRadius,
      completedAt: completedAt,
    );
  }

  @override
  void write(BinaryWriter writer, Checkpoint obj) {
    writer.write(obj.id);
    writer.write(obj.name);
    writer.write(obj.address);
    writer.write(obj.latitude);
    writer.write(obj.longitude);
    writer.write(obj.isCompleted);
    writer.write(obj.orderIndex);
    writer.write(obj.geofenceRadius);
    writer.write(obj.completedAt?.toIso8601String());
  }
}
