import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/utils/distance_utils.dart';
import '../models/checkpoint.dart';
import '../providers/checklist_provider.dart';
import '../../route/providers/route_provider.dart';
import 'add_place_sheet.dart';

class ChecklistWidget extends ConsumerWidget {
  final ScrollController scrollController;

  const ChecklistWidget({super.key, required this.scrollController});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(checklistProvider);
    final routeState = ref.watch(routeProvider);

    return Column(
      children: [
        _DragHandle(
          checkpoints: state.checkpoints,
          completedCount: state.completedCount,
          isTracking: state.isTrackingActive,
          geofenceRadius: state.geofenceRadius,
          routeState: routeState,
          ref: ref,
        ),
        if (state.error != null) _ErrorBanner(message: state.error!, ref: ref),
        Expanded(
          child: state.isLoading
              ? const Center(child: CircularProgressIndicator())
              : state.isEmpty
                  ? _EmptyState(ref: ref)
                  : _CheckpointList(
                      scrollController: scrollController,
                      checkpoints: state.checkpoints,
                      nextTargetId: state.nextTarget?.id,
                      ref: ref,
                    ),
        ),
      ],
    );
  }
}

// ── Drag handle + header ───────────────────────────────────────────────────────

class _DragHandle extends StatelessWidget {
  final List<Checkpoint> checkpoints;
  final int completedCount;
  final bool isTracking;
  final double geofenceRadius;
  final RouteState routeState;
  final WidgetRef ref;

  const _DragHandle({
    required this.checkpoints,
    required this.completedCount,
    required this.isTracking,
    required this.geofenceRadius,
    required this.routeState,
    required this.ref,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Center(
          child: Container(
            margin: const EdgeInsets.only(top: 12),
            width: 40,
            height: 4,
            decoration: BoxDecoration(
              color: Colors.grey[300],
              borderRadius: BorderRadius.circular(2),
            ),
          ),
        ),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'Le tue tappe',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      if (checkpoints.isNotEmpty)
                        Text(
                          '$completedCount/${checkpoints.length} completate',
                          style: TextStyle(
                            fontSize: 12,
                            color: completedCount == checkpoints.length
                                ? Colors.green
                                : Colors.grey[600],
                          ),
                        ),
                    ],
                  ),
                  const Spacer(),
                  _ActionButtons(
                    checkpoints: checkpoints,
                    isTracking: isTracking,
                    routeState: routeState,
                    ref: ref,
                  ),
                ],
              ),
              if (routeState.hasRoute) ...[
                const SizedBox(height: 6),
                _RouteInfoChips(
                  routeState: routeState,
                  geofenceRadius: geofenceRadius,
                ),
              ],
            ],
          ),
        ),
        const Divider(height: 1),
      ],
    );
  }
}

class _ActionButtons extends StatelessWidget {
  final List<Checkpoint> checkpoints;
  final bool isTracking;
  final RouteState routeState;
  final WidgetRef ref;

  const _ActionButtons({
    required this.checkpoints,
    required this.isTracking,
    required this.routeState,
    required this.ref,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        // Calculate / recalculate route
        if (checkpoints.length >= 2)
          IconButton(
            tooltip: routeState.hasRoute
                ? 'Ricalcola percorso'
                : 'Calcola percorso ottimale',
            icon: routeState.isCalculating
                ? const SizedBox(
                    width: 20,
                    height: 20,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  )
                : Icon(
                    Icons.alt_route,
                    color: routeState.hasRoute ? Colors.blue : Colors.grey[700],
                  ),
            onPressed: routeState.isCalculating
                ? null
                : () => ref
                    .read(routeProvider.notifier)
                    .calculateRoute(checkpoints),
          ),

        // Tracking toggle
        if (checkpoints.isNotEmpty)
          IconButton(
            tooltip: isTracking
                ? 'Disattiva rilevamento GPS'
                : 'Attiva rilevamento GPS automatico',
            icon: Icon(
              isTracking ? Icons.location_on : Icons.location_off,
              color: isTracking ? Colors.green : Colors.grey[700],
            ),
            onPressed: () {
              if (isTracking) {
                ref.read(checklistProvider.notifier).stopTracking();
              } else {
                ref.read(checklistProvider.notifier).startTracking();
              }
            },
          ),

        // Add place
        IconButton(
          tooltip: 'Aggiungi tappa',
          icon: const Icon(Icons.add_location_alt),
          onPressed: () async {
            final place = await showAddPlaceSheet(context);
            if (place != null) {
              await ref.read(checklistProvider.notifier).addCheckpoint(place);
              // Auto-calculate if >= 2 stops
              final updated = ref.read(checklistProvider).checkpoints;
              if (updated.length >= 2) {
                ref.read(routeProvider.notifier).calculateRoute(updated);
              }
            }
          },
        ),

        // More options
        if (checkpoints.isNotEmpty)
          PopupMenuButton<String>(
            tooltip: 'Altro',
            icon: const Icon(Icons.more_vert),
            onSelected: (value) async {
              switch (value) {
                case 'reset':
                  final confirm = await _confirmDialog(
                    context,
                    'Azzera spunte',
                    'Vuoi resettare tutte le spunte mantenendo le tappe?',
                  );
                  if (confirm) {
                    ref.read(checklistProvider.notifier).resetAllCheckpoints();
                  }
                case 'clear':
                  final confirm = await _confirmDialog(
                    context,
                    'Elimina tutto',
                    'Vuoi eliminare tutte le tappe? Questa azione non è reversibile.',
                  );
                  if (confirm) {
                    ref.read(checklistProvider.notifier);
                    for (final c in [...checkpoints]) {
                      await ref
                          .read(checklistProvider.notifier)
                          .removeCheckpoint(c.id);
                    }
                    ref.read(routeProvider.notifier).clearRoute();
                  }
                case 'settings':
                  _showSettingsSheet(context, ref);
              }
            },
            itemBuilder: (_) => [
              const PopupMenuItem(value: 'reset', child: Text('Azzera spunte')),
              const PopupMenuItem(value: 'settings', child: Text('Impostazioni GPS')),
              const PopupMenuDivider(),
              const PopupMenuItem(
                value: 'clear',
                child: Text('Elimina tutte le tappe',
                    style: TextStyle(color: Colors.red)),
              ),
            ],
          ),
      ],
    );
  }

  Future<bool> _confirmDialog(
      BuildContext context, String title, String content) async {
    return await showDialog<bool>(
          context: context,
          builder: (ctx) => AlertDialog(
            title: Text(title),
            content: Text(content),
            actions: [
              TextButton(
                  onPressed: () => Navigator.pop(ctx, false),
                  child: const Text('Annulla')),
              FilledButton(
                  onPressed: () => Navigator.pop(ctx, true),
                  child: const Text('Conferma')),
            ],
          ),
        ) ??
        false;
  }

  void _showSettingsSheet(BuildContext context, WidgetRef ref) {
    showModalBottomSheet(
      context: context,
      builder: (_) => const _SettingsSheet(),
    );
  }
}

class _RouteInfoChips extends StatelessWidget {
  final RouteState routeState;
  final double geofenceRadius;

  const _RouteInfoChips(
      {required this.routeState, required this.geofenceRadius});

  @override
  Widget build(BuildContext context) {
    final result = routeState.result!;
    return Wrap(
      spacing: 8,
      children: [
        _Chip(
          icon: Icons.straighten,
          label: DistanceUtils.formatDistance(
              result.totalDistanceMeters.toDouble()),
          color: Colors.blue,
        ),
        _Chip(
          icon: Icons.timer_outlined,
          label: DistanceUtils.formatDuration(result.totalDurationSeconds),
          color: Colors.indigo,
        ),
        _Chip(
          icon: result.isApiOptimized ? Icons.verified : Icons.offline_bolt,
          label: result.isApiOptimized ? 'Ottimizzato' : 'Locale',
          color: result.isApiOptimized ? Colors.green : Colors.orange,
        ),
        _Chip(
          icon: Icons.radar,
          label: '${geofenceRadius.toInt()} m',
          color: Colors.teal,
        ),
      ],
    );
  }
}

class _Chip extends StatelessWidget {
  final IconData icon;
  final String label;
  final Color color;

  const _Chip({required this.icon, required this.label, required this.color});

  @override
  Widget build(BuildContext context) {
    return Chip(
      materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
      padding: const EdgeInsets.symmetric(horizontal: 4),
      avatar: Icon(icon, size: 14, color: color),
      label: Text(label, style: TextStyle(fontSize: 11, color: color)),
      backgroundColor: color.withOpacity(0.1),
      side: BorderSide(color: color.withOpacity(0.3)),
    );
  }
}

// ── Checkpoint list ────────────────────────────────────────────────────────────

class _CheckpointList extends StatelessWidget {
  final ScrollController scrollController;
  final List<Checkpoint> checkpoints;
  final String? nextTargetId;
  final WidgetRef ref;

  const _CheckpointList({
    required this.scrollController,
    required this.checkpoints,
    required this.nextTargetId,
    required this.ref,
  });

  @override
  Widget build(BuildContext context) {
    final sorted = [...checkpoints]
      ..sort((a, b) => a.orderIndex.compareTo(b.orderIndex));

    return ReorderableListView.builder(
      scrollController: scrollController,
      padding: const EdgeInsets.only(bottom: 16),
      itemCount: sorted.length,
      onReorder: (oldIndex, newIndex) {
        ref
            .read(checklistProvider.notifier)
            .reorderCheckpoints(oldIndex, newIndex);
      },
      itemBuilder: (context, index) {
        final checkpoint = sorted[index];
        final isNext = checkpoint.id == nextTargetId;
        return _CheckpointTile(
          key: ValueKey(checkpoint.id),
          checkpoint: checkpoint,
          index: index + 1,
          isNext: isNext,
          ref: ref,
        );
      },
    );
  }
}

class _CheckpointTile extends StatelessWidget {
  final Checkpoint checkpoint;
  final int index;
  final bool isNext;
  final WidgetRef ref;

  const _CheckpointTile({
    super.key,
    required this.checkpoint,
    required this.index,
    required this.isNext,
    required this.ref,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: isNext
              ? Colors.orange
              : checkpoint.isCompleted
                  ? Colors.green.withOpacity(0.4)
                  : Colors.grey.withOpacity(0.2),
          width: isNext ? 2 : 1,
        ),
        color: checkpoint.isCompleted
            ? Colors.green.withOpacity(0.05)
            : isNext
                ? Colors.orange.withOpacity(0.05)
                : Colors.white,
      ),
      child: ListTile(
        contentPadding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
        leading: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            ReorderableDragStartListener(
              index: index - 1,
              child: const Icon(Icons.drag_handle, color: Colors.grey, size: 20),
            ),
            const SizedBox(width: 4),
            _IndexBadge(
              index: index,
              isCompleted: checkpoint.isCompleted,
              isNext: isNext,
            ),
          ],
        ),
        title: Text(
          checkpoint.name,
          style: TextStyle(
            fontWeight: isNext ? FontWeight.bold : FontWeight.normal,
            decoration: checkpoint.isCompleted
                ? TextDecoration.lineThrough
                : TextDecoration.none,
            color: checkpoint.isCompleted ? Colors.grey : Colors.black87,
          ),
        ),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              checkpoint.address,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: const TextStyle(fontSize: 12),
            ),
            if (checkpoint.isCompleted && checkpoint.completedAt != null)
              Text(
                '✅ ${_formatTime(checkpoint.completedAt!)}',
                style: const TextStyle(fontSize: 11, color: Colors.green),
              ),
            if (isNext)
              const Text(
                '🎯 Prossima tappa',
                style: TextStyle(
                  fontSize: 11,
                  color: Colors.orange,
                  fontWeight: FontWeight.w600,
                ),
              ),
          ],
        ),
        trailing: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Checkbox(
              value: checkpoint.isCompleted,
              activeColor: Colors.green,
              onChanged: (_) => ref
                  .read(checklistProvider.notifier)
                  .toggleCheckpoint(checkpoint.id),
            ),
            PopupMenuButton<String>(
              icon: const Icon(Icons.more_vert, size: 18),
              padding: EdgeInsets.zero,
              onSelected: (value) {
                if (value == 'delete') {
                  ref
                      .read(checklistProvider.notifier)
                      .removeCheckpoint(checkpoint.id);
                }
              },
              itemBuilder: (_) => [
                const PopupMenuItem(
                  value: 'delete',
                  child: Text('Elimina tappa',
                      style: TextStyle(color: Colors.red)),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  String _formatTime(DateTime dt) {
    return '${dt.hour.toString().padLeft(2, '0')}:'
        '${dt.minute.toString().padLeft(2, '0')}';
  }
}

class _IndexBadge extends StatelessWidget {
  final int index;
  final bool isCompleted;
  final bool isNext;

  const _IndexBadge(
      {required this.index, required this.isCompleted, required this.isNext});

  @override
  Widget build(BuildContext context) {
    Color bg;
    Widget child;
    if (isCompleted) {
      bg = Colors.green;
      child = const Icon(Icons.check, color: Colors.white, size: 14);
    } else if (isNext) {
      bg = Colors.orange;
      child = Text('$index',
          style: const TextStyle(
              color: Colors.white, fontWeight: FontWeight.bold, fontSize: 12));
    } else {
      bg = Colors.grey[400]!;
      child = Text('$index',
          style: const TextStyle(
              color: Colors.white, fontWeight: FontWeight.bold, fontSize: 12));
    }
    return Container(
      width: 26,
      height: 26,
      decoration: BoxDecoration(color: bg, shape: BoxShape.circle),
      alignment: Alignment.center,
      child: child,
    );
  }
}

// ── Empty state ────────────────────────────────────────────────────────────────

class _EmptyState extends StatelessWidget {
  final WidgetRef ref;

  const _EmptyState({required this.ref});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.map_outlined, size: 64, color: Colors.grey[300]),
            const SizedBox(height: 16),
            const Text(
              'Nessuna tappa aggiunta',
              style:
                  TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
            ),
            const SizedBox(height: 8),
            Text(
              'Aggiungi i luoghi che vuoi visitare. L\'app ottimizzerà il percorso e spunterà automaticamente le tappe quando ci arrivi.',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 14, color: Colors.grey[600]),
            ),
            const SizedBox(height: 24),
            FilledButton.icon(
              onPressed: () async {
                final place = await showAddPlaceSheet(context);
                if (place != null) {
                  ref.read(checklistProvider.notifier).addCheckpoint(place);
                }
              },
              icon: const Icon(Icons.add_location_alt),
              label: const Text('Aggiungi prima tappa'),
            ),
          ],
        ),
      ),
    );
  }
}

// ── Error banner ───────────────────────────────────────────────────────────────

class _ErrorBanner extends StatelessWidget {
  final String message;
  final WidgetRef ref;

  const _ErrorBanner({required this.message, required this.ref});

  @override
  Widget build(BuildContext context) {
    return MaterialBanner(
      backgroundColor: Colors.red[50],
      content: Text(message, style: const TextStyle(color: Colors.red)),
      leading: const Icon(Icons.error_outline, color: Colors.red),
      actions: [
        TextButton(
          onPressed: () => ref.read(checklistProvider.notifier).clearError(),
          child: const Text('OK'),
        ),
      ],
    );
  }
}

// ── Settings sheet ─────────────────────────────────────────────────────────────

class _SettingsSheet extends ConsumerStatefulWidget {
  const _SettingsSheet();

  @override
  ConsumerState<_SettingsSheet> createState() => _SettingsSheetState();
}

class _SettingsSheetState extends ConsumerState<_SettingsSheet> {
  late double _radius;

  @override
  void initState() {
    super.initState();
    _radius = ref.read(checklistProvider).geofenceRadius;
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(24),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Impostazioni GPS',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 20),
          Text(
            'Raggio di arrivo: ${_radius.toInt()} m',
            style: const TextStyle(fontWeight: FontWeight.w500),
          ),
          Slider(
            value: _radius,
            min: 20,
            max: 500,
            divisions: 48,
            label: '${_radius.toInt()} m',
            onChanged: (v) => setState(() => _radius = v),
          ),
          const Text(
            'L\'app segnerà la tappa come completata quando ti trovi entro questo raggio.',
            style: TextStyle(fontSize: 12, color: Colors.grey),
          ),
          const SizedBox(height: 24),
          Row(
            mainAxisAlignment: MainAxisAlignment.end,
            children: [
              TextButton(
                onPressed: () => Navigator.pop(context),
                child: const Text('Annulla'),
              ),
              const SizedBox(width: 8),
              FilledButton(
                onPressed: () {
                  ref
                      .read(checklistProvider.notifier)
                      .setGeofenceRadius(_radius);
                  Navigator.pop(context);
                },
                child: const Text('Salva'),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
