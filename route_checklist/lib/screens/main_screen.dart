import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:geolocator/geolocator.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import '../features/map/widgets/route_map.dart';
import '../features/checklist/widgets/checklist_widget.dart';
import '../features/checklist/providers/checklist_provider.dart';
import '../features/route/providers/route_provider.dart';

class MainScreen extends ConsumerStatefulWidget {
  const MainScreen({super.key});

  @override
  ConsumerState<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends ConsumerState<MainScreen> {
  // GlobalKey typed to the public RouteMapState so we can call moveTo()
  final GlobalKey<RouteMapState> _mapKey = GlobalKey<RouteMapState>();
  final DraggableScrollableController _sheetController =
      DraggableScrollableController();

  bool _isSheetExpanded = false;

  @override
  void dispose() {
    _sheetController.dispose();
    super.dispose();
  }

  void _toggleSheet() {
    final target = _isSheetExpanded ? 0.35 : 0.85;
    _sheetController.animateTo(
      target,
      duration: const Duration(milliseconds: 300),
      curve: Curves.easeInOut,
    );
    setState(() => _isSheetExpanded = !_isSheetExpanded);
  }

  Future<void> _centerOnUser() async {
    try {
      final perm = await Geolocator.checkPermission();
      if (perm == LocationPermission.denied ||
          perm == LocationPermission.deniedForever) return;
      final pos = await Geolocator.getCurrentPosition(
        locationSettings:
            const LocationSettings(accuracy: LocationAccuracy.high),
      );
      _mapKey.currentState?.moveTo(LatLng(pos.latitude, pos.longitude));
    } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    final checklistState = ref.watch(checklistProvider);
    final routeState = ref.watch(routeProvider);

    // Show route-level errors as snackbars
    ref.listen(routeProvider, (_, next) {
      if (next.error != null) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(next.error!),
            backgroundColor: Colors.red,
            action: SnackBarAction(
              label: 'OK',
              textColor: Colors.white,
              onPressed: () =>
                  ref.read(routeProvider.notifier).clearError(),
            ),
          ),
        );
        ref.read(routeProvider.notifier).clearError();
      }
    });

    return Scaffold(
      body: Stack(
        children: [
          // ── Full-screen map background ────────────────────────────────────
          SizedBox.expand(
            child: RouteMap(key: _mapKey),
          ),

          // ── Top status bar ────────────────────────────────────────────────
          SafeArea(
            child: Align(
              alignment: Alignment.topCenter,
              child: _TopBar(
                checklistState: checklistState,
                routeState: routeState,
              ),
            ),
          ),

          // ── Floating action buttons (right side, above sheet) ─────────────
          Positioned(
            right: 12,
            bottom: MediaQuery.of(context).size.height * 0.35 + 8,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                _MapFab(
                  tooltip: 'La mia posizione',
                  icon: Icons.my_location,
                  onTap: _centerOnUser,
                ),
                const SizedBox(height: 8),
                _MapFab(
                  tooltip:
                      _isSheetExpanded ? 'Riduci lista' : 'Espandi lista',
                  icon: _isSheetExpanded
                      ? Icons.keyboard_arrow_down
                      : Icons.keyboard_arrow_up,
                  onTap: _toggleSheet,
                ),
              ],
            ),
          ),

          // ── Draggable checklist sheet ─────────────────────────────────────
          DraggableScrollableSheet(
            controller: _sheetController,
            initialChildSize: 0.35,
            minChildSize: 0.10,
            maxChildSize: 0.90,
            snap: true,
            snapSizes: const [0.10, 0.35, 0.90],
            builder: (context, scrollController) {
              return Container(
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius:
                      const BorderRadius.vertical(top: Radius.circular(20)),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.15),
                      blurRadius: 12,
                      offset: const Offset(0, -4),
                    ),
                  ],
                ),
                child: ChecklistWidget(scrollController: scrollController),
              );
            },
          ),
        ],
      ),
    );
  }
}

// ── Top bar ────────────────────────────────────────────────────────────────────

class _TopBar extends StatelessWidget {
  final ChecklistState checklistState;
  final RouteState routeState;

  const _TopBar({
    required this.checklistState,
    required this.routeState,
  });

  @override
  Widget build(BuildContext context) {
    final allDone =
        checklistState.allCompleted && checklistState.checkpoints.isNotEmpty;

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      child: Row(
        children: [
          // Title pill
          Container(
            padding:
                const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(24),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.12),
                  blurRadius: 8,
                  offset: const Offset(0, 2),
                ),
              ],
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(
                  allDone ? Icons.celebration : Icons.route,
                  size: 18,
                  color: allDone
                      ? Colors.green
                      : Theme.of(context).primaryColor,
                ),
                const SizedBox(width: 6),
                Text(
                  allDone
                      ? 'Percorso completato!'
                      : routeState.isCalculating
                          ? 'Calcolo percorso...'
                          : 'Route Checklist',
                  style: const TextStyle(
                    fontWeight: FontWeight.w600,
                    fontSize: 14,
                  ),
                ),
              ],
            ),
          ),
          const Spacer(),
          // GPS active badge
          if (checklistState.isTrackingActive)
            Container(
              padding:
                  const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
              decoration: BoxDecoration(
                color: Colors.green,
                borderRadius: BorderRadius.circular(20),
                boxShadow: [
                  BoxShadow(
                    color: Colors.green.withOpacity(0.3),
                    blurRadius: 8,
                  ),
                ],
              ),
              child: const Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(Icons.location_on, color: Colors.white, size: 14),
                  SizedBox(width: 4),
                  Text(
                    'GPS attivo',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 12,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ],
              ),
            ),
        ],
      ),
    );
  }
}

// ── Round floating action button ───────────────────────────────────────────────

class _MapFab extends StatelessWidget {
  final String tooltip;
  final IconData icon;
  final VoidCallback onTap;

  const _MapFab(
      {required this.tooltip, required this.icon, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Tooltip(
      message: tooltip,
      child: GestureDetector(
        onTap: onTap,
        child: Container(
          width: 44,
          height: 44,
          decoration: BoxDecoration(
            color: Colors.white,
            shape: BoxShape.circle,
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.15),
                blurRadius: 8,
                offset: const Offset(0, 2),
              ),
            ],
          ),
          child: Icon(icon, size: 22, color: Colors.grey[800]),
        ),
      ),
    );
  }
}
