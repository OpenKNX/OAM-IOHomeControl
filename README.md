# OAM-IO-Homecontrol

OpenKNX application module for an io-homecontrol-to-KNX gateway.

This repository assembles the `OFM-IO-Homecontrol` firmware module with the required OpenKNX base and optional application modules into complete build targets and ETS products. The detailed io-homecontrol functionality itself is documented in the firmware module.

## Scope of this repository

This OAM provides:

- PlatformIO environments for the supported hardware targets
- OpenKNX module composition and registration
- ETS product generation for the complete application
- Integration of `OFM-IO-Homecontrol` with OpenKNX Logic, FunctionBlocks, Network and ConfigTransfer modules
- Release/build scripts and target-specific configuration

## Module documentation

For all io-homecontrol specific details, use the `OFM-IO-Homecontrol` documentation:

- Application description: `doc/Applikationsbeschreibung-IoHomecontrol.md` in the `OFM-IO-Homecontrol` module
- Pairing and commissioning notes: module pairing/debug documentation
- Communication objects and DPTs: module application description
- Radio/protocol diagnostics: module README and service documentation

## Hardware Targets

| Board | Radio | KNX | Environment |
| --- | --- | --- | --- |
| XIAO ESP32-S3 | SX1262 | TP | `develop_OpenKNX_XIAO_S3_SX1262_TP`, `release_OpenKNX_XIAO_S3_SX1262_TP` |
| XIAO ESP32-S3 | SX1262 | IP (WiFi) | `develop_OpenKNX_XIAO_S3_SX1262_IP`, `release_OpenKNX_XIAO_S3_SX1262_IP` |
| XIAO ESP32-S3 | SX1276 | IP (WiFi) | `develop_OpenKNX_XIAO_S3_SX1276_IP` |
| ESP32-S3 dev board (wired) | SX1276 | IP (WiFi) | `develop_OpenKNX_ESP32_S3_DEV_SX1276_IP` |
| REG1 ESP DevBoard v00.11 | SX1276 | TP | `develop_OpenKNX_REG1_ESP_V00_11_SX1276_TP`, `release_OpenKNX_REG1_ESP_V00_11_SX1276_TP` |
| REG1 ESP DevBoard v00.11 | SX1276 | IP (LAN) | `develop_OpenKNX_REG1_ESP_V00_11_SX1276_IP`, `release_OpenKNX_REG1_ESP_V00_11_SX1276_IP` |

All targets use ESP32 with 8 MB flash.

## Included Modules

| Module | Description |
| --- | --- |
| OFM-IO-Homecontrol | io-homecontrol radio, protocol, channel logic and ETS integration |
| OFM-LogicModule | OpenKNX logic module |
| OFM-FunctionBlocks | OpenKNX function blocks |
| OFM-Network | Network support for KNX IP targets |
| OFM-ConfigTransfer | ConfigTransfer pages included in the ETS product |
| OGM-Common | OpenKNX base framework |

Firmware module registration order in `main.cpp`:

1. Network, conditional on KNX IP targets
2. IoHomecontrol
3. Logic
4. FunctionBlocks

## Building

### Prerequisites

- PlatformIO
- OpenKNXproducer

### Generate ETS Product

```bash
OpenKNXproducer create --Debug -h include/knxprod.h src/IoHomecontrol
```

This generates:

- `include/knxprod.h` for firmware compilation
- `src/IoHomecontrol.knxprod` for ETS import

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
    hardware.h          Hardware pin definitions and LED defaults
    versions.h          Firmware version strings
    knxprod.h           Generated parameter/KO macros
  src/
    main.cpp            Module registration and startup
    IoHomecontrol.xml   Application XML
    IoHomecontrol.conf.xml
    IoHomecontrol.base.xml
  lib/                  Symlinked OFM/OGM dependencies
  scripts/              Build automation
  platformio.ini
  platformio.custom.ini Build environments and radio pin maps
```

## Version

`0.1.0`
