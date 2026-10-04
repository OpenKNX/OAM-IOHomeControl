# Reverse-engineering implementation checkpoint — 2026-10-04

Target branch: `v1dev-KLFDocumentation`. Local commits by Franz Reisenhofer; no remote publication.

| OFM commit | Change |
| --- | --- |
| `bcfffc5` | Version-3 header codec, 32-byte declaration ceiling and trailer capacity preflight |
| `5b53297` | Assigned-channel recognition API, guided ETS type adoption, preservation of custom/expert settings |
| `bcf0ec9` | Sorted, bounded sparse MP/FP representation; existing FP1–FP3 command bytes retained |
| `b8800e7` | SX1276 preamble byte units and hardware conformance boundaries |
| `c43edb2` | Module 0.2.0 and matching module XML version |

OAM composes application 3.6 and requires module 0.2. The generated header differs only in `MAIN_ApplicationVersion` (53→54) and `IOHC_ModuleVersion` (1→2); all parameter offsets, channel layout and KNX object numbers remain unchanged. The flash serialization format remains unchanged.

## Validation

- Native full suite: 513 passed, 0 failed (baseline: 506).
- ETS XML/UI checks: 32 passed.
- Actual ETS JavaScript recognition tests: 7 passed, executed with QuickJS. Covers old firmware, invalid response schema, unknown profile, unpaired/1W channels, manual profile overrides, binary-only recognition and repeated import preservation.
- Existing native SX1262 device-error/PHY suites pass; these do not qualify SX1276 RF behavior.
- OpenKNXproducer 4.3.12 (official macOS arm64 build): internal integrity checks and project-20 XML schema validation pass. Its helper-function/help-link warnings are nonfatal.
- PlatformIO builds pass: `develop_OpenKNX_XIAO_S3_SX1276_TP`, `release_OpenKNX_XIAO_S3_SX1276_TP`, `develop_OpenKNX_XIAO_S3_SX1276_IP`.

The installed x86 producer and PlatformIO Python lacking LZMA could not run on this host. Validation used temporary arm64 producer and Python/PlatformIO tools, with the existing local module checkouts/toolchain. No system tool replacement or firmware flashing was performed. ETS is unavailable on this host, so a signed `.knxprod` and an actual ETS project-update/device-download check were not produced. The XML and generated C++ header were validated and compiled.

## Remaining work

1. Measure SX1276 preamble/sync/payload and turnaround on hardware, including low-power wake, 1W enrollment, DIO4 absent, scan hold, CRC failure and contention. Do not equate software-UART prefix counts with FSK preamble registers.
2. Validate controller version-3 authentication/continuation producers against an original-device exchange. Codec support alone does not switch outgoing controller defaults.
3. Audit atomic flash commit and replay-counter reservation/recovery under power loss and repeated restart. No universal peer replay-window/resynchronization behavior has been assumed.
4. Add exact product-scoped MP/FP codecs and KNX presentation in bounded groups. The sparse representation encoder does not enable arbitrary high-FP writes or decode unresolved temperature/mode/timer schemas.
5. Run real ETS commissioning and project migration with expert overrides and configured group addresses, then generate the signed product on an ETS-equipped system. Verify reset/recovery and authenticated status with real peers before release.

In ETS, read **Status / Erkennung lesen** after successful 2W pairing, then use **Erkannten Gerätetyp übernehmen** and program the application. Reading status alone does not change settings. A nonzero manual profile blocks inferred category changes; 1W and unknown profiles require manual selection. Names, manual power policy, suspension and discovery settings survive recognition and import.
