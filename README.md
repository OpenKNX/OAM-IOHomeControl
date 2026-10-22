# OAM-IOHomeControl

OpenKNX application for an io-homecontrol-to-KNX gateway.

This repository assembles the [OFM-IOHomeControl](https://github.com/OpenKNX/OFM-IOHomeControl) function module with the required OpenKNX base and application function modules into complete build targets and ETS products. The io-homecontrol functionality itself is documented in the [OFM-IOHomeControl](https://github.com/OpenKNX/OFM-IOHomeControl) function module.

## Functions / OpenKNX modules

| Function | Module | ETS application manual | Description |
| --- | --- | --- | --- |
| io-homecontrol gateway | [OFM-IOHomeControl](https://github.com/OpenKNX/OFM-IOHomeControl) | [Applikationsbeschreibung IoHomecontrol](https://github.com/OpenKNX/OFM-IOHomeControl/blob/v1/doc/Applikationsbeschreibung-IoHomecontrol.md) | 16 channels for io-homecontrol devices: radio, protocol, pairing and ETS integration |
| 99 logic channels | [OFM-LogicModule](https://github.com/OpenKNX/OFM-LogicModule) | [Applikationsbeschreibung Logik](https://github.com/OpenKNX/OFM-LogicModule/blob/v1/doc/Applikationsbeschreibung-Logik.md) | Pre- and post-processing of events and conversion between DPTs |
| 15 function blocks | [OFM-FunctionBlocks](https://github.com/OpenKNX/OFM-FunctionBlocks) | [Applikationsbeschreibung FunctionBlocks](https://github.com/OpenKNX/OFM-FunctionBlocks/blob/v1/doc/Applikationsbeschreibung-FunctionBlocks.md) | Grouping of channels into reusable function blocks |
| Network | [OFM-Network](https://github.com/OpenKNX/OFM-Network) | [Applikationsbeschreibung Netzwerk](https://github.com/OpenKNX/OFM-Network/blob/v1/doc/Applikationsbeschreibung-Netzwerk.md) | Network support for KNX IP targets |
| Configuration transfer | [OFM-ConfigTransfer](https://github.com/OpenKNX/OFM-ConfigTransfer) | [Applikationsbeschreibung ConfigTransfer](https://github.com/OpenKNX/OFM-ConfigTransfer/blob/v1/doc/Applikationsbeschreibung-ConfigTransfer.md) | Copy, export and import of configuration examples |
| OpenKNX base | [OGM-Common](https://github.com/OpenKNX/OGM-Common) | – | OpenKNX base framework |

## Module documentation

For all io-homecontrol specific details, use the [OFM-IOHomeControl](https://github.com/OpenKNX/OFM-IOHomeControl) documentation:

- Application description, communication objects and DPTs
- Pairing and commissioning notes
- VELUX KUX/KLI enrollment finalizer and troubleshooting guidance
- Radio/protocol diagnostics

The October 2026 interoperability updates preserve legacy result codes while decoding
packed `0xFE` errors, stop definitive key-transfer refusals, and bind pairing
responses to the peer, channel, key and deadline. Pull-key mode is an explicit
verified diagnostic; it never automatically pushes or stores the received key.
A name reply on its own after a missing `0x33` does not establish key ownership.
Normal push pairing first tries up to two challenged name reads before another
key-init; only a correlated reply after the matching authentication response
permits recovery, and successful durable storage is still required. Nina Config
State is observed without enabling an unqualified responder or automatic key pull.

For confirmed MOTO 1000 io devices, enable the existing endpoint-only option;
other garage models retain their own positioning capabilities. Battery evidence
uses the existing low-battery KO. `iohc battery CH status` shows Full/Normal/Low
or unknown/not reported, distinguishes historical evidence, and adds no polling
or percentage estimate. Atlantic pull, Nina responder sequencing and KLI/KUX wake
timing still require the documented hardware tests.

## Atlantic heating (application 4.7)

Private heating registers require a confirmed Atlantic 52/1 actuator and its own channel key. The separate 1023/0 pairing node is never assigned as a heater. Generic heat pumps and existing VELUX/Somfy commissioning retain their own protocol paths.

Normal pairing and discovery now recognize the Atlantic 1023/0 pairing node and offer the matching pull command. Normal pairing stops before pushing a key. Read the ETS channel status to see “Atlantic Pull angeboten” and the exact command. This temporary advice changes no channel assignment, metadata or key; it expires after three minutes and is shown only for an empty 2W channel. Pull and subsequent assignment remain explicit.

On a selected empty channel, the ETS Atlantic Pull button (or `iohc heating pair CHANNEL [PAIRNODE]`) stages a temporary key, verifies its proof and probes a candidate heater. A silent pairing-node-plus-one probe triggers six bounded SPE attempts: three long-preamble, low-power attempts followed by three short-preamble attempts, each listening across all three frequencies. Pairing and heater addresses can be unrelated after reset. Review the separate pairing/heater identities in ETS status, then explicitly use the verified-heater assignment button (or `iohc heating assign CHANNEL SESSION`). Only a verified heater and successful durable write complete assignment; the global system key and occupied channels remain unchanged. Generic diagnostic pull does not assign a device.

`iohc heating read NODE REGISTER` and `refresh CHANNEL` request measured values. The optional ETS bank starts at KO 1800, with ten objects per channel: room temperature, setpoint feedback, raw mode, validity bitmap, heating activity, window contact, detection enable/status, optional maximum setpoint and refresh. Unknown or faulty measurements clear validity without publishing a fabricated zero. Setpoint and mode writes require a separate readback. Polling starts disabled; `poll CHANNEL SECONDS` or ETS can opt in, subject to production airtime limits and backoff. See the [module manual](https://github.com/OpenKNX/OFM-IOHomeControl/blob/v1dev-KLFDocumentation/doc/Applikationsbeschreibung-IoHomecontrol.md#private-atlantic-heizung-ab-46) for the calculated 16-heater airtime plan.

Back up the ETS project before upgrading from 4.5. Existing channel parameter offsets and KO numbers remain fixed, but legacy Kn+24 becomes read-only window feedback, Kn+22 uses DPT 5.010 raw mode codes, and Kn+21 reports the measured setpoint. Remove old window-write group addresses and check mode links. Presence Kn+23 remains reserved. Import online metadata and download the application to expose qualified heating functions.

Application 4.7 adds a separate Home/Away bank at `1960 + 3*(CHANNEL-1)`: command (DPT 1.001, 1=Home/0=Away), last authenticated acknowledged command (DPT 1.001), and command status (DPT 5.010; 0=unknown). Explicitly confirm the **AGILIA IO display model on the actual device** in ETS; this setting defaults off and additionally requires manufacturer 12/profile 52/1 metadata and a paired channel key. Generic `I2G_Actuator` names do not identify the model. Other Atlantic/Thermor products are not qualified by this option.

Home/Away writes register `0x0110`; `0x0101` remains separate and read-only. An ACK confirms the command exchange, never room occupancy, heating effect or a measured setpoint. Optional explicit readback is reported separately; there is no automatic polling, mode change or command replay after reboot. Startup status is unknown. Existing 4.6 KO numbers, parameter offsets and the 580-byte per-channel cache are preserved; the new model flag uses a spare bit. Back up the ETS project and verify group associations during upgrade.

The source evidence is [Laberning #176, b4b749353cfaa586868926e84d953eff6db4ff13](https://github.com/laberning/home_io_control/commit/b4b749353cfaa586868926e84d953eff6db4ff13). Public captures and synthetic security tests validate software paths. Real SX1262/SX1276 RF tests, original-heater BASIC/AUTO/PROG behavior (including at least 30 minutes in AUTO), power-cut scenarios, signed ETS export and real ETS migration/download campaigns remain unrun release gates. See the OFM release-evidence template; a successful build or ACK cannot fill these gates.

## Hardware targets

| Board | Radio | KNX | Environment |
| --- | --- | --- | --- |
| XIAO ESP32-S3 | SX1262 | TP | `develop_OpenKNX_XIAO_S3_SX1262_TP`, `release_OpenKNX_XIAO_S3_SX1262_TP` |
| XIAO ESP32-S3 | SX1262 | IP (WiFi) | `develop_OpenKNX_XIAO_S3_SX1262_IP`, `release_OpenKNX_XIAO_S3_SX1262_IP` |
| XIAO ESP32-S3 | SX1276 | IP (WiFi) | `develop_OpenKNX_XIAO_S3_SX1276_IP` |
| ESP32-S3 dev board (wired) | SX1276 | IP (WiFi) | `develop_OpenKNX_ESP32_S3_DEV_SX1276_IP` |
| REG1 ESP DevBoard v00.11 | SX1276 | TP | `develop_OpenKNX_REG1_ESP_V00_11_SX1276_TP`, `release_OpenKNX_REG1_ESP_V00_11_SX1276_TP` |
| REG1 ESP DevBoard v00.11 | SX1276 | IP (LAN) | `develop_OpenKNX_REG1_ESP_V00_11_SX1276_IP`, `release_OpenKNX_REG1_ESP_V00_11_SX1276_IP` |

All targets use ESP32 with 8 MB flash.

## Building

This repository follows the standard OpenKNX build process. See the [OpenKNX wiki](https://github.com/OpenKNX/OpenKNX/wiki) for the general toolchain setup (PlatformIO, OpenKNXproducer, dependency restore).

Generate the ETS product and build a firmware target:

```bash
OpenKNXproducer create --Debug -h include/knxprod.h src/IoHomecontrol
pio run -e develop_OpenKNX_XIAO_S3_SX1262_TP
```

A complete release build is produced with:

```powershell
scripts/Build-Release.ps1 -Release
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md).
