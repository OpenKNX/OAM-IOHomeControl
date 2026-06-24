# OAM-IOHomeControl

OpenKNX application for an io-homecontrol-to-KNX gateway.

This repository assembles the [OFM-IOHomeControl](https://github.com/OpenKNX/OFM-IOHomeControl) function module with the required OpenKNX base and application function modules into complete build targets and ETS products. The io-homecontrol functionality itself is documented in the [OFM-IOHomeControl](https://github.com/OpenKNX/OFM-IOHomeControl) function module.

## Functions / OpenKNX modules

| Function | Module | Description |
| --- | --- | --- |
| io-homecontrol gateway | [OFM-IOHomeControl](https://github.com/OpenKNX/OFM-IOHomeControl) | 16 channels for io-homecontrol devices: radio, protocol, pairing and ETS integration |
| 100 logic channels | [OFM-LogicModule](https://github.com/OpenKNX/OFM-LogicModule) | Pre- and post-processing of events and conversion between DPTs |
| 15 function blocks | [OFM-FunctionBlocks](https://github.com/OpenKNX/OFM-FunctionBlocks) | Grouping of channels into reusable function blocks |
| Network | [OFM-Network](https://github.com/OpenKNX/OFM-Network) | Network support for KNX IP targets |
| Configuration transfer | [OFM-ConfigTransfer](https://github.com/OpenKNX/OFM-ConfigTransfer) | Copy, export and import of configuration examples |
| OpenKNX base | [OGM-Common](https://github.com/OpenKNX/OGM-Common) | OpenKNX base framework |

Function module registration order in [src/main.cpp](src/main.cpp):

1. Network, conditional on KNX IP targets
2. IoHomecontrol
3. Logic
4. FunctionBlocks

## Module documentation

For all io-homecontrol specific details, use the [OFM-IOHomeControl](https://github.com/OpenKNX/OFM-IOHomeControl) documentation:

- Application description, communication objects and DPTs
- Pairing and commissioning notes
- Radio/protocol diagnostics

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
