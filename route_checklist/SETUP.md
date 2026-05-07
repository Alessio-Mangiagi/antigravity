# Route Checklist — Setup Guide

## 1. Prerequisiti

| Strumento | Versione minima |
|-----------|----------------|
| Flutter   | 3.10.0         |
| Dart      | 3.0.0          |
| Android SDK | API 23 (minSdk) |
| Xcode     | 14+ (solo macOS, per iOS) |

Verifica: `flutter doctor -v`

---

## 2. Google Cloud Console — API Keys

### 2.1 Crea un progetto e abilita le API

1. Vai su [console.cloud.google.com](https://console.cloud.google.com)
2. Crea un nuovo progetto o selezionane uno esistente
3. Menu → API e servizi → Libreria → abilita:
   - **Maps SDK for Android**
   - **Maps SDK for iOS**
   - **Directions API** (ottimizzazione percorso)
   - **Places API** (autocompletamento indirizzi)

### 2.2 Crea le API Key

Menu → API e servizi → Credenziali → Crea credenziali → Chiave API

**Consigliato:** crea chiavi separate per Android/iOS con restrizioni di app.

### 2.3 Inserisci la chiave nel codice

Sostituisci `YOUR_GOOGLE_MAPS_API_KEY` in **3 file**:

| File | Punto |
|------|-------|
| `lib/core/constants/app_constants.dart` | `googleMapsApiKey` |
| `android/app/src/main/AndroidManifest.xml` | `meta-data android:value` |
| `ios/Runner/AppDelegate.swift` | `GMSServices.provideAPIKey(...)` |

---

## 3. Installazione dipendenze

```bash
cd route_checklist
flutter pub get
```

---

## 4. Esecuzione

### Android (emulatore o dispositivo fisico)

```bash
# Lista dispositivi disponibili
flutter devices

# Esegui su un dispositivo specifico
flutter run -d <device_id>

# Build release APK
flutter build apk --release
```

### iOS (solo macOS)

```bash
cd ios && pod install && cd ..
flutter run -d <ios_device_id>

# Build IPA
flutter build ios --release
```

---

## 5. Test del Geofencing

### Su emulatore Android

1. Apri l'emulatore → ⋮ (Extended Controls) → Location
2. Inserisci le coordinate di una tappa aggiunta
3. Clicca "Set Location" — il geofence si attiverà entro 5 secondi
4. La tappa si spunta automaticamente e appare una notifica

### Su dispositivo fisico

1. Attiva il GPS del telefono in modalità "Precisione elevata"
2. Recati fisicamente nel raggio della tappa (default 75 m)
3. L'app rileva l'arrivo e spunta la tappa anche se è in background (schermo acceso)

**Nota background tracking:** l'implementazione attuale funziona con l'app in foreground. Per il tracking completo in background (schermo spento) aggiungere `flutter_background_service` o `flutter_background_geolocation` (piano a pagamento).

---

## 6. Struttura cartelle

```
lib/
├── core/
│   ├── constants/app_constants.dart   # API keys, default values
│   ├── utils/distance_utils.dart      # Haversine, polyline decoder, TSP
│   └── errors/app_errors.dart         # Custom exceptions
├── features/
│   ├── route/
│   │   ├── models/
│   │   │   ├── place.dart             # Luogo con Hive adapter
│   │   │   ├── place_adapter.dart     # Hive TypeAdapter (manuale)
│   │   │   └── route_result.dart      # Risultato ottimizzazione
│   │   ├── services/routing_service.dart  # Directions + Places API
│   │   └── providers/route_provider.dart  # Riverpod state
│   ├── map/
│   │   └── widgets/route_map.dart     # GoogleMap + markers + polyline
│   └── checklist/
│       ├── models/
│       │   ├── checkpoint.dart        # Tappa con stato completamento
│       │   └── checkpoint_adapter.dart
│       ├── services/
│       │   ├── geofence_service.dart  # Monitoraggio posizione + notifiche
│       │   └── storage_service.dart   # Hive CRUD
│       ├── providers/checklist_provider.dart  # Riverpod state
│       └── widgets/
│           ├── checklist_widget.dart  # Lista drag-and-drop + controlli
│           └── add_place_sheet.dart   # Bottom sheet aggiunta tappa
└── screens/main_screen.dart           # Layout principale (mappa + sheet)
```

---

## 7. Flusso utente

```
1. Apri app → mappa centrata sulla posizione utente
2. Scorri su il pannello inferiore (checklist)
3. Tap + (icona) → cerca un indirizzo o inserisci coordinate GPS
4. Aggiungi almeno 2 tappe
5. L'app calcola automaticamente il percorso ottimale via Directions API
6. Tap icona "percorso" per ricalcolare manualmente
7. Tap icona GPS per attivare il rilevamento automatico
8. Cammina/guida → le tappe si spuntano automaticamente con notifica
9. Drag-and-drop per riordinare manualmente le tappe
10. Menu ⋮ → "Azzera spunte" per ricominciare il percorso
```

---

## 8. Colori marker sulla mappa

| Colore | Significato |
|--------|------------|
| 🔵 Azzurro | Prima tappa (partenza) |
| 🟣 Viola | Ultima tappa (arrivo) |
| 🟠 Arancione | Prossima tappa da raggiungere |
| 🔴 Rosso | Tappa intermedia non ancora raggiunta |
| 🟢 Verde | Tappa completata |

---

## 9. Limitazioni e costi API

### Google Maps Platform — Free Tier (mensile)

| API | Gratis | Costo extra |
|-----|--------|-------------|
| Maps SDK | Illimitato | Gratis |
| Directions API | 40.000 req | $5/1000 req |
| Places Autocomplete | 100.000 req | $2.83/1000 req |
| Place Details | 100.000 req | $17/1000 req |

**Alternativa gratuita:** sostituire Directions API con OSRM (`http://router.project-osrm.org/route/v1/driving/`). Modificare `RoutingService._optimizeWithApi()` per chiamare OSRM. L'ottimizzazione TSP rimarrebbe locale (nearest-neighbour).

### Limiti tecnici attuali

- **Geofencing solo in foreground**: con schermo spento il tracking si interrompe. Soluzione: `flutter_background_service`.
- **Max waypoints Google Directions**: 25 waypoints intermedi per chiamata (piano standard). Per percorsi più lunghi: suddividere le chiamate.
- **Nessun export GPX**: aggiungibile facilmente iterando `RouteResult.polylinePoints`.

---

## 10. Troubleshooting

### "PlatformException: Google Maps API key not configured"
→ Controlla `AndroidManifest.xml` e `AppDelegate.swift`. La chiave deve essere attiva.

### "MissingPluginException" su geolocator
→ Riesegui `flutter pub get` e riavvia l'app (cold restart, non hot reload).

### Notifiche non arrivano su Android 13+
→ L'app richiede il permesso `POST_NOTIFICATIONS` al primo avvio. Accettalo.

### Hive: "Box already open"
→ Già gestito: `main()` apre le box una sola volta prima di `runApp`.

### Routing fallback locale vs API
→ Se la Directions API non è abilitata o la quota è esaurita, il routing usa il nearest-neighbour locale (senza strade, distanza lineare). Indicato dal chip "Locale" nell'UI.
