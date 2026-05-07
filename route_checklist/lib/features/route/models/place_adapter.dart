part of 'place.dart';

// typeId = 0
class PlaceAdapter extends TypeAdapter<Place> {
  @override
  final int typeId = 0;

  @override
  Place read(BinaryReader reader) {
    final id = reader.read() as String;
    final name = reader.read() as String;
    final address = reader.read() as String;
    final latitude = reader.read() as double;
    final longitude = reader.read() as double;
    return Place(
      id: id,
      name: name,
      address: address,
      latitude: latitude,
      longitude: longitude,
    );
  }

  @override
  void write(BinaryWriter writer, Place obj) {
    writer.write(obj.id);
    writer.write(obj.name);
    writer.write(obj.address);
    writer.write(obj.latitude);
    writer.write(obj.longitude);
  }
}
