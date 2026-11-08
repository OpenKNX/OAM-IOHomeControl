# Qualified model build evidence

Local validation on 2026-11-08, OFM pin `e12953ddef77d5198b9518a9c17658ae8c4cfe7f`. This is local build evidence, not remote CI or physical device acceptance. Eleven dependency revisions were checked against their actual local Git HEADs; other pins remain unchanged, including HardwareConfig v1 at 0c5a94d.

| Target | RAM / 327680 bytes | Application flash / 2621440 bytes |
|---|---:|---:|
| REG1/SX1276-IP release | 124260 | 1994994 |
| XIAO ESP32-S3/SX1262-IP release | 126400 | 1947842 |
| XIAO ESP32-S3/SX1262-IP debug | 126408 | 1978250 |

All three complete builds succeeded. REG1 and S3 debug use 56 bytes more static RAM than their prior successful 124204/126352-byte comparison builds. Opt-in sensor, name-proof and diagnostic polling state is allocated lazily. Debug RF remains unlimited; production admission/authentication regressions pass.

The normal shared PlatformIO cache changed during the first attempts, producing missing esptool/header/assembler errors. Final builds use an isolated core at `/tmp/alignment-pio-core`, with PlatformIO 6.1.19, platform 54.3.21, native arm64 Xtensa GCC 14.2.0_20241119, Arduino 3.2.1, ESP-IDF libraries 5.4.0+858a988d6e and esptool 5.0.2. The official esptool archive matches SHA-256 `1b30d7f78281f315a6cd82b4553711fa7f4ca25986abd21415d0cbd2e75d63f1`. GitHub asset API downloads recovered release-URL 504 errors. Machine-local `platform_packages` paths select those same exact official tool versions; they add no firmware flags and are not committed as repository dependencies. The exact local build configuration and tool/dependency manifests are retained in Findings.

Reproduction in the prepared review worktree:

```sh
PLATFORMIO_CORE_DIR=/tmp/alignment-pio-core /Users/juliagrabner/.platformio/penv/bin/pio run \
  -e release_OpenKNX_REG1_ESP_V00_11_SX1276_IP \
  -e release_OpenKNX_XIAO_S3_SX1262_IP \
  -e develop_OpenKNX_XIAO_S3_SX1262_IP
python3 tools/check_heating_model_layout.py
```

Native validation: 921 protocol/controller/exchange tests, zero failures, plus full storage/corpus/importer/privacy/mutation/publication/schema checks and selected production tests in debug/release. Final firmware logs and artifact hashes are archived at `Velocet/Findings/2026-11-08-qualified-sensors-and-atlantic/`.

OpenKNXproducer 4.3.12 successfully generated the versioned header/expanded XML. The configured XSD and ETS are unavailable here, so no signed `.knxprod` exists. [Pending device and release gates](qualified-model-application.md) apply before merge or release. No upload, physical RF command or test-device motion was performed.
