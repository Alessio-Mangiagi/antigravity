import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'core/constants/app_constants.dart';
import 'features/route/models/place.dart';
import 'features/checklist/models/checkpoint.dart';
import 'screens/main_screen.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialise Hive
  await Hive.initFlutter();
  Hive.registerAdapter(PlaceAdapter());
  Hive.registerAdapter(CheckpointAdapter());
  await Hive.openBox<Checkpoint>(AppConstants.checkpointsBox);
  await Hive.openBox<dynamic>(AppConstants.settingsBox);

  runApp(
    const ProviderScope(
      child: RouteChecklistApp(),
    ),
  );
}

class RouteChecklistApp extends StatelessWidget {
  const RouteChecklistApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Route Checklist',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorSchemeSeed: const Color(0xFF1976D2),
        useMaterial3: true,
        appBarTheme: const AppBarTheme(
          centerTitle: true,
          elevation: 0,
        ),
      ),
      home: const MainScreen(),
    );
  }
}
