# OAM-IO-Homecontrol

OpenKNX application module for an io-homecontrol-to-KNX gateway. The application integrates Somfy and other io-homecontrol devices into KNX by means of ESP32-based controllers with SX1262 or SX1276 radio hardware.

## Overview

This OAM integrates the `OFM-IO-Homecontrol` firmware module into a complete OpenKNX application and provides the following functions:

- Up to 16 io-homecontrol channels, each paired with one physical device
- 13 device types with type-specific ETS parameters and KNX communication objects
- Channel-based pairing with key exchange and persistent flash storage
- Scene support for all device types (up to 10 scenes per channel)
- Cozy thermostat integration (temperature, operating mode, presence, window contact)
- Status feedback via device push or configurable polling interval
- 1W (unidirectional) and 2W (bidirectional) protocol mode per channel
- Discovery, optional runtime post-pairing SPE discovery, and network scan via KNX communication objects
- Remote control observation and logging
- OpenKNX Logic and FunctionBlocks modules included

## Hardware Targets

| Board | Radio | KNX | Environment |
| --- | --- | --- | --- |
| XIAO ESP32-S3 | SX1262 | TP (NanoBCU) | `develop_OpenKNX_XIAO_S3_SX1262_TP`, `release_OpenKNX_XIAO_S3_SX1262_TP` |
| XIAO ESP32-S3 | SX1262 | IP (WiFi) | `develop_OpenKNX_XIAO_S3_SX1262_IP`, `release_OpenKNX_XIAO_S3_SX1262_IP` |
| XIAO ESP32-S3 | SX1276 | IP (WiFi) | `develop_OpenKNX_XIAO_S3_SX1276_IP` |
| ESP32-S3 dev board (wired) | SX1276 | IP (WiFi) | `develop_OpenKNX_ESP32_S3_DEV_SX1276_IP` |
| REG1 ESP DevBoard v00.11 | SX1276 | TP | `develop_OpenKNX_REG1_ESP_V00_11_SX1276_TP`, `release_OpenKNX_REG1_ESP_V00_11_SX1276_TP` |
| REG1 ESP DevBoard v00.11 | SX1276 | IP (LAN) | `develop_OpenKNX_REG1_ESP_V00_11_SX1276_IP`, `release_OpenKNX_REG1_ESP_V00_11_SX1276_IP` |

All targets use ESP32 with 8 MB flash.

## Device Types

Each channel is assigned a device type in ETS that controls which parameters and KNX objects are visible:

| Value | Type | Scene Parameters |
| --- | --- | --- |
| 0 | Generisch | Position, Aktion, Lamelle |
| 1 | Jalousie / Rollladen | Position, Aktion, Lamelle |
| 2 | Fenster | Position, Aktion, Lamelle |
| 3 | Markise | Position, Aktion, Lamelle |
| 4 | Garagentor | Position, Aktion, Lamelle |
| 5 | Thermostat | Temperatur (7-28 C), Modus |
| 6 | Licht | Ein/Aus |
| 7 | Tor | Position, Aktion, Lamelle |
| 8 | Schloss | Ein/Aus |
| 9 | Sonnenschutz horizontal | Position, Aktion, Lamelle |
| 10 | Vorhangschiene | Position, Aktion, Lamelle |
| 11 | Lueftung | Position, Aktion, Lamelle |
| 12 | Schalter | Ein/Aus |

Position-capable types (0-4, 7, 9-11) expose drive time, direction, position, slat, favorite, ventilation, and step objects. Thermostat (5) exposes Cozy temperature setpoint/feedback, operating mode, presence, and window contact. Licht/Schloss/Schalter (6, 8, 12) use position as on/off.

## KNX Communication Objects

### Global Objects (module offset)

| KO# | Name | DPT | Direction |
| --- | --- | --- | --- |
| 20 | Modulstatus | 1.001 | Read |
| 21 | Discovery starten | 1.001 | Write |
| 22 | Discovery aktiv | 1.001 | Read |
| 23 | Netzwerk-Scan | 1.001 | Write |
| 24 | Netzwerk-Scan aktiv | 1.001 | Read |
| 25 | Beobachtete Fernbedienung | 12.001 | Read |

### Per-Channel Objects (25 KOs per channel)

| KO | Name | DPT | Direction | Visibility |
| --- | --- | --- | --- | --- |
| K0 | Position | 5.001 | Write | Position types |
| K1 | Position Rueckmeldung | 5.001 | Read | Position types |
| K2 | Auf/Ab | 1.008 | Write | Position types |
| K3 | Stopp | 1.001 | Write | Position types |
| K4 | Status | 1.001 | Read | All |
| K5 | Lamelle | 5.001 | Write | Jalousie only (1) |
| K6 | Lamelle Rueckmeldung | 5.001 | Read | Jalousie only (1) |
| K7 | Favorit | 1.001 | Write | Position types |
| K8 | Lueftung | 1.001 | Write | Fenster, Lueftung (2, 11) |
| K9 | Pairing-Status | 1.001 | Read | All |
| K10 | Batterie | 5.001 | Read | All |
| K11 | RSSI | 5.001 | Read | All |
| K12 | Sperre | 1.001 | Write | Schloss (8) |
| K13 | Fehler | 5.010 | Read | All |
| K14 | Szene | 17.001 | Write | All (when scenes > 0) |
| K15 | Szenensteuerung | 18.001 | Write | All (when scenes > 0) |
| K16 | Wind/Regen-Alarm | 1.005 | Write | Position types |
| K17 | Schritt/Langbetrieb | 1.008 | Write | Position types |
| K18 | Cozy Temperatur Sollwert | 9.001 | Write | Thermostat (5) |
| K19 | Cozy Temperatur Rueckmeldung | 9.001 | Read | Thermostat (5) |
| K20 | Cozy Betriebsmodus | 20.102 | Write | Thermostat (5) |
| K21 | Cozy Praesenz | 1.018 | Write | Thermostat (5) |
| K22 | Cozy Fensterkontakt | 1.019 | Write | Thermostat (5) |
| K23 | Geraetename | 16.001 | Read | All |
| K24 | Geraetetyp-Code | 7.001 | Read | All |

## Scenes

Each channel supports up to 10 KNX scenes (DPT 17.001 / 18.001). The number of active scenes is configured via the `Anzahl Szenen` dropdown per channel. Setting it to `Keine` disables scene handling for that channel.

Scene parameters depend on the device type:

- **Position types** (0-4, 7, 9-11): Action (Position / Favorit / Lueftung), target position (0-100%), and slat position (0-100%) per scene.
- **Thermostat** (5): Temperature (7-28 C) and operating mode (Auto / Manuell / Programm / Aus) per scene.
- **Licht / Schloss / Schalter** (6, 8, 12): On/Off state per scene.

Scene recall is triggered via K14. Scene store (via K15 with store bit) is supported for position types only; thermostat, light, lock, and switch scenes are ETS-configured only.

## ETS Parameters

### Global Page

- **Anzahl io-homecontrol Kanäle** — Number of visible channels (1 to 16)
- **Fernbedienungs-Beobachtung aktivieren** — Enable remote control address logging to KO#25

### Per Channel

- **Beschreibung** — Free-text channel name (40 characters)
- **Geraetetyp** — Device type selection (determines visible parameters and KOs)
- **Anlernmodus** — Pairing mode: Anlernen (pair) or Entfernen (unpair)
- **Status-Abfrageintervall (Fallback)** — Polling interval: Deaktiviert / 30s / 1min / 5min / 15min / 30min; used as fallback when the device does not push status updates on its own
- **Verhalten nach Neustart** — Power-on: Nichts tun / Status abfragen / Letzte Position anfahren
- **Protokollmodus** — 2W (bidirectional) or 1W (unidirectional)
- **1W Aktor-Node-ID** — Visible for 1W channels; decimal actuator node ID used for first-time blind 1W pairing (`0` = unset)
- **Fahrzeit oeffnen / schliessen** — Travel times for position interpolation (position types only)
- **Fahrtrichtung** — Invert motor direction (position types only)
- **Anzahl Szenen** — Scene count: Keine / 1-10
- Per-scene parameters (type-dependent, see Scenes section above)

## Pairing

Pairing is channel-based and stored persistently in flash. The intended ETS workflow is as follows:

1. Set the number of active channels on the global page.
2. Open the target channel, set device type and description.
3. For 1W devices, set protocol mode to `1W` and enter the actuator node ID in `1W Aktor-Node-ID`.
4. Set pairing mode to `Anlernen`.
5. Start the pairing action while ETS is online.
6. Check the channel's Pairing-Status KO (K9) afterwards.

On develop builds, an ETS-triggered pairing or unpair action also writes an immediate message to the serial console, for example `ETS: pairing started for channel N` or `ETS: channel N unpaired`.

Pairing performs discovery, key exchange, flash persistence, and optionally sends SetConfig1 to enable automatic device feedback. The assignment remains valid across reboots.
Optional SPE/sub-device discovery can be enabled at runtime with `iohc autospe on`. When enabled, a successful pairing schedules an encrypted `0x2A` discovery pass after the controller returns to idle. Discovered SPE nodes are logged and recorded in the observed/scan buffers, while channel assignments remain manual.
For 2W channels, the controller sends discovery confirmation (`0x2C/0x2D`), attempts the documented pull-key exchange (`0x38 -> 0x32 -> 0x3C -> 0x3D`), and then continues with the established push pairing path (`0x31 -> 0x3C -> 0x32 -> (0x2C | 0x33)`) before the optional SetConfig1 step.

For 1W channels, pairing is a blind learning session on channel 2: the gateway sends repeated `0x39` exclusion frames followed by repeated `0x30` encrypted-key frames. Because 1W learning has no response path, the target actuator node ID must be known in advance. The firmware takes this address from the ETS parameter `1W Aktor-Node-ID` when the channel is not yet paired; the serial or API pairing command can still override it with an explicit hex address.

To unpair, set the channel's pairing mode to `Entfernen` and trigger the action. The console commands (`iohc pair NN`, `iohc pair NN AABBCC`, `iohc unpair NN`) can also be used without ETS.

For a concise field guide aimed at end users with real io-homecontrol devices, refer to [PAIRING-DEBUG-GUIDE.md](PAIRING-DEBUG-GUIDE.md). A short German version is available in [PAIRING-DEBUG-GUIDE.de.md](PAIRING-DEBUG-GUIDE.de.md).

## Included Modules

| Module | Description |
| --- | --- |
| OFM-IO-Homecontrol | io-homecontrol radio, protocol, channel logic, ETS integration |
| OFM-LogicModule | OpenKNX logic module (up to 100 channels) |
| OFM-FunctionBlocks | Function blocks (up to 15 channels) |
| OFM-Network | Network support (WiFi/LAN for KNX IP targets) |
| OFM-ConfigTransfer | ConfigTransfer pages included in the ETS product |
| OGM-Common | OpenKNX base framework (v1.7) |

Firmware module registration order in `main.cpp`: Network (slot 0, conditional on KNX IP), IoHomecontrol (slot 1), Logic (slot 2), FunctionBlocks (slot 3).

## Debug Logging And Diagnostics

For troubleshooting, a develop build should be used. The develop environments enable `OPENKNX_DEBUG`; release environments do not. The serial monitor runs at 115200 baud.

Typical workflow:

1. Build and flash a develop environment.
2. Open a serial monitor: `pio device monitor -b 115200`.
3. Watch boot and runtime logs while triggering pairing or commands from ETS.
4. Use the built-in console commands for targeted checks.

For a compact step-by-step capture sequence for a real pairing attempt, refer to [PAIRING-DEBUG-GUIDE.md](PAIRING-DEBUG-GUIDE.md). For German-speaking users, refer to [PAIRING-DEBUG-GUIDE.de.md](PAIRING-DEBUG-GUIDE.de.md).

### Console Commands

| Command | Description |
| --- | --- |
| `iohc help` | Show available commands |
| `iohc status` | All channels with paired state and node ID |
| `iohc status NN` | Detailed status for one channel |
| `iohc pair NN` | Start 2W pairing, or 1W pairing using the ETS target node ID or current stored node ID |
| `iohc pair NN AABBCC` | Start 1W pairing for channel NN with known actuator node ID `AABBCC` |
| `iohc pair cancel` | Cancel active pairing |
| `iohc unpair NN` | Remove pairing for channel NN |
| `iohc discover` | Discover io-homecontrol devices on the radio |
| `iohc discover spe` | Run encrypted SPE/sub-device discovery and record responses |
| `iohc autospe on\|off\|status` | Runtime-only automatic SPE discovery after successful pairing |
| `iohc send NN PP` | Send position PP to channel NN |
| `iohc set1w NN` | Mark channel NN as 1W before or after pairing |
| `iohc set2w NN` | Mark channel NN as 2W before or after pairing |
| `iohc cozy temp NN TT` | Set thermostat target temperature in tenths of a degree (`70`-`280`) |
| `iohc cozy mode NN MM` | Set thermostat mode (`0`-`3`) |
| `iohc cozy presence NN 0/1` | Set Cozy presence flag |
| `iohc cozy window NN 0/1` | Set Cozy window-contact flag |
| `iohc cozy poweron NN` | Send Cozy power-on command |
| `iohc cozy midnight NN` | Send Cozy midnight sync |
| `iohc remote list` | List tracked remotes |
| `iohc remote add ADDR NAME` | Add a tracked remote by hex address |
| `iohc remote del ADDR` | Remove a tracked remote |
| `iohc remote link ADDR DEV` | Link a device node to a tracked remote |
| `iohc remote unlink ADDR DEV` | Unlink a device node from a tracked remote |
| `iohc remote observed` | Show recently observed remote addresses |
| `iohc scan start` | Start passive multi-frequency network scan |
| `iohc scan stop` | Stop passive network scan |
| `iohc scan dump` | Dump captured packets from the scan buffer |
| `iohc scan stats` | Show per-node scan statistics |
| `iohc radio` | Show radio health summary (init/state/RSSI/frequency/queue/duty) |
| `iohc radio raw` | Show raw SX1262 register readback; standard SX1262 mode should show chip sync `57FD99` |
| `iohc radio txtest` | Send a minimal SX1262 TX test payload |
| `iohc radio sweep [N]` | Run `N` sweep rounds across all 3 io-homecontrol frequencies |
| `iohc radio soak [S]` | Run a time-budgeted TX soak for `S` seconds across all 3 io-homecontrol frequencies |
| `iohc proto selftest` | Run in-memory frame/CRC/HMAC/key-transfer/parser/flash sanity checks without RF traffic |

The OpenKNX Diagnose KO (DPT 16.001, 14 characters) forwards short commands into the same parser. Use it for remote checks like `iohc status` or `iohc radio` without a USB connection. Longer commands like `iohc pair cancel` or `iohc pair NN AABBCC` require the serial console.

### Radio Health Check

Use `iohc radio` to verify whether the radio path looks alive:

- `init=1` means the SX1262/SX1276 driver initialized successfully.
- `radio=Rx` or `radio=Idle` is normal during standby operation.
- `lastRssi` changes and `lastResp` gets updated when frames are seen.
- `freq` shows the current receive hop index; it should change when RX scan is active.
- `q` shows pending transmit queue depth.
- `duty` shows the current worst-case duty-cycle usage over the active 1-hour window.
- for SX1262 builds, `initErr`, `status`, `cmdStat`, and `busyTO` provide extra bring-up detail:
  - `initErr=1` / `busyTO=1`: BUSY pin stayed high too long
  - `initErr=2`: post-reset `GET_STATUS` returned an invalid chip mode outside the SX1262 range (`STDBY_RC`, `STDBY_XOSC`, `FS`, `RX`, `TX`)
  - `initErr=3`: chip answered initially, but configuration failed later
  - `status=0x..`: raw SX1262 `GET_STATUS` byte captured during init
  - `cmdStat=..`: SX1262 `CommandStatus` field decoded from status bits `3:1`
  - `initDev=0x....[....]`: cached SX1262 device-error word captured at the end of init before the driver clears it for runtime use, followed by decoded Semtech error names in the serial log
  - `devErr=0x....[....]`: most recent live SX1262 device-error word seen by the driver, followed by decoded Semtech error names in the serial log
  - `tcxo=NNNNus/M`: last TCXO startup delay used and the number of startup attempts taken during init
  - `rf=0x..`: active RF-switch surfaces as a bitmask (`0x01` shared GPIO, `0x02` DIO2, `0x04` RX_EN, `0x08` TX_EN)
  - `txS` / `txD`: cumulative TX start / TX done counts
  - `rxS`: cumulative RX start count
  - `irq`: cumulative SX1262 IRQ observations processed by the driver
  - `poll`: IRQ observations found by polling `GET_IRQ_STATUS` without a DIO1 edge
  - `pre` / `preOnly` / `sync` / `rxD`: cumulative preamble IRQs, preamble-only IRQs, sync-word-valid IRQs, and RX-done IRQs
  - `rxReadFail`: RX status or FIFO read failures that forced an immediate RX re-arm
  - `crc` / `to`: cumulative CRC-error and timeout IRQ counts
  - `lastIrq=0x....`: last raw SX1262 IRQ status word seen by the driver

- `iohc radio raw` on a normal SX1262 io-homecontrol build should show `sync=57FD99`. That is the chip-level sync remap of the protocol sync `55FF33` used by the software-emulated io-homecontrol PHY.

Practical checks:

1. Boot the device and run `iohc radio` once. Confirm `init=1`.
2. Run `iohc discover` and then `iohc radio` again. Queue depth and controller state should change temporarily.
3. If you have live io-homecontrol traffic nearby, start `iohc scan start`, wait a few seconds, then use `iohc scan dump` or `iohc scan stats`.
4. If packets are captured there but normal commands still fail, the RF receive path is likely working and the issue is higher up in protocol/pairing/authentication.
5. Without any io-homecontrol devices, use `iohc proto selftest` to verify frame serialization, declared-length handling, CRC/HMAC slicing, `0x32`/`0x3D` key-transfer framing, parser rejection, flash count clamping, 1W key encryption, and the Velocet-style 1W/2W key-exchange regression vectors locally.
6. Without any io-homecontrol devices, use `iohc radio sweep 2` or `iohc radio soak 10` to stress TX on all three io-homecontrol frequencies and confirm clean SX1262 completion status.

## Status LED

The module registers the `io-homecontrol Status` LED function. Default assignment: Info LED 2. Reassignable via the Common module Info LEDs page.

| Pattern | Meaning |
| --- | --- |
| Slow pulse | Running, no channel paired |
| Steady on | Running, at least one channel paired |
| Fast blink | Pairing in progress |
| One short flash | Pairing completed successfully |
| Two-blink with pause | Pairing failed (check serial log) |
| Short acknowledgment flash | Paired channel count changed |

## Building

### Prerequisites

- PlatformIO
- OpenKNXproducer (for ETS product generation)

### Generate ETS Product

```bash
OpenKNXproducer create --Debug -h include/knxprod.h src/IoHomecontrol
```

This generates `include/knxprod.h` (required for firmware compilation) and `src/IoHomecontrol.knxprod` (ETS import file).

### Build Firmware

```bash
# Develop build for XIAO S3 + SX1262 + KNX TP
pio run -e develop_OpenKNX_XIAO_S3_SX1262_TP

# Release build for REG1 + SX1276 + KNX TP
pio run -e release_OpenKNX_REG1_ESP_V00_11_SX1276_TP
```

### Release Build

```powershell
scripts/Build-Release.ps1 -Release
```

## Project Structure

```text
OAM-IO-Homecontrol/
  include/
    hardware.h          Hardware pin definitions, LED defaults
    versions.h          Firmware version strings
    knxprod.h           Generated parameter/KO macros
  src/
    main.cpp            Module registration and startup
    IoHomecontrol.xml   Application XML (includes share + templ)
    IoHomecontrol.conf.xml
    IoHomecontrol.base.xml
  lib/                  Symlinked OFM/OGM dependencies
  scripts/              Build automation
  platformio.ini
  platformio.custom.ini Build environments and radio pin maps
```

## Version

`0.1.0`
