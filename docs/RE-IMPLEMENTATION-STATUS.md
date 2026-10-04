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

## Continuation: reservation persistence and exact read semantics

| OFM commit | Change |
| --- | --- |
| `df301af` | Force sequence-window flash saves; share the real allocation policy between production channels and native tests |
| `efa04f2` | Add OVPd projection FP9 and window-lock FP1 read semantics with explicit provenance and strict enum decoding |
| `c3d69b9` | Pause module RF/controller state machines while KNX configuration is unavailable |
| `69ef65a` | Use the actual version-dependent command offset for key redaction; keep malformed extended frames opaque |

The local OGM-Common (`da2c6ff`) flash audit found a default **180,000 ms** write throttle in `Flash/Default.h`; `Default::save(false)` silently returns inside that interval. The old sequence-window renewal used this throttled call, despite requiring persistence before transmission. It now uses `save(true)` at renewal, retaining the sixteen-value reservation policy. No-transmission restarts do not reserve another window. Wraparound is covered by allocator tests; acceptance of wraparound by every peer is not claimed. Production and native channels now execute the same allocation helper instead of maintaining duplicate implementations.

Even `save(true)` returns while `knx.configured()` is false. The module loop now waits for configured state before running controller, radio diagnostic and workflow state machines. This does not retract a hardware transmission already in progress when ETS starts programming.

The source audit also confirms that ESP32 uses **one storage slot** in the current shared backend; the alternate-slot implementation is conditional on RP2040. ESP32 sector erase/rewrite and the `void` save/commit API do not establish an atomic rollback or successful-write acknowledgement for OFM. This continuation closes throttle/configuration defects, not the remaining power-cut recovery gate. A journaled backend or independent durable identity-bound reservation journal still needs design and hardware fault injection.

The OVPd supplement leaves the Appendix-2 table and generic actuator capability flags unchanged. Exact profile2/subprofile2 has projection FP9 metadata; its units and write path remain unspecified. Exact profile9/subprofile1 has window-security FP1:0 daylocked,1 homesecure,2 secured. Other values are unknown, including special-value sentinels. Diagnostic reads classify the enum as discrete and log its name without publishing position KOs. New semantic descriptors remain non-writable. Sliding-window, pergola and heat-pump expansions remain gated by exact product identity and qualified state/transport paths.

Frame-level log redaction now reads the command at byte10 for valid version3 headers and at byte8 for ordinary versions0–2. Extended `0x30`/`0x32` payloads cannot bypass the key filter due to an address byte being misread as the command. Invalid or truncated version3 headers display only the control bytes plus a redaction marker, since their payload offsets are ambiguous. Payload-level redaction remains unchanged.

Continuation checks: **521 native tests,33 XML/UI/source checks and7 executed ETS JavaScript regressions pass**. These include a throttled native flash adapter and the shared production allocator, not a real flash power-cut test. Firmware build results are recorded after the final checks below.

Final continuation firmware checks pass for `develop_OpenKNX_XIAO_S3_SX1276_IP`, `release_OpenKNX_XIAO_S3_SX1276_TP` and `develop_OpenKNX_XIAO_S3_SX1276_TP`, including the configuration guard and redaction fix. There are no ETS XML, parameter-memory, KO-layout or flash-format changes in this continuation, so application/module versions remain3.6/0.2.0. `dependencies.txt` advances the local OFM pin to`69ef65a`. Existing compiler warnings outside the changes remain; no flash power-cut, radio peer or real ETS migration test is claimed.

## Continuation: version-3 recipient exchanges and product codecs

Separate OFM commits, authored and committed locally as Franz Reisenhofer:

| Commit | Implementation |
| --- | --- |
| `daf44e1` | Normalize recipient replies in all key-extraction phases, including authenticated node verification |
| `121531f` | Checked temperature codecs and offline `iohc codec temp` diagnostics |
| `b55b272` | Checked RGB chromaticity and tunable-white representation conversions |

The recipient rules come from STM32 `0x0800FE5C–0x0800FFA8`: use the active local identity, reply to the request source, retain PRIORITY, clear LOW_POWER/ROUTED, produce BEACON from incoming ROUTED/BEACON, mirror version3 and swap ACK-request/response on non-START replies. START replies clear ACK bits. Generated3D has END; otherwise incoming PRIORITY suppresses END, generated3C suppresses END, and other replies have END. Ordinary request versions1/2 normalize to reply version0. The new helper consumes parsed 2W frames and preserves command/data. The real controller regression covers discovery, confirmation, key recovery, node verification and the independent command/data HMAC transcript. Controller/master-originated authentication policy remains separate and still needs original-peer version3 qualification.

Temperature selectors identify explicit OVPd definitions, not inferred commercial products: heatpump `0x160000`, heating-interface `0xE0000`, generic-heater `0x340100`, atlantic-heater `0x34010C`, atlantic-dhw-v2 `0x33000C`, atlantic-dhw-ck `0x1000033000C`. Index0 means MP. Heatpump MP is −40..80°C (tenths), FP8 rounds to whole degrees. Heating-interface MP, generic FP12/13 and DHW-v2 MP require supplied minimum/maximum centikelvin bounds. Generic FP13 uses FP12 comfort minus the FP13 raw difference; it is not an independent absolute setpoint. Atlantic FP12 uses28015..30115CK; FP13 uses27515..28215CK, a numeric2..9°C quantity whose physical eco/setback interpretation is still gated. The centikelvin DHW variant is raw/100−273.15. Raw words above51200, missing/invalid context, unknown slots and nonfinite/out-of-range inverse inputs fail without changing the output. Coupled generic FP13, heatpump FP8 and centikelvin DHW inverse writes are not enabled.

Console syntax: `iohc codec temp PRODUCT INDEX RAW16 [MIN_CK MAX_CK [COMFORT_RAW]]`. Product names are those above; raw words use hex, bounds use decimal centikelvin. It converts offline, without RF transmission, flash saves or KO publication. It retains the existing configured-KNX console guard.

RGB definitions `0x60100`, `0x60102`, `0x10000060102` use the retained RGBToVector/vectorToRGB matrices, inverse MP brightness, FP10=u and FP11=v, without gamma correction. Black explicitly yields off MP and no chromaticity, avoiding the source's0/0. Tunable-white definitions `0x60202`, `0x10000060202` use FP14 over2000..6500K. The source producer's second argument is raw MP passthrough, not a percentage. Positive truncation is an explicit lighting encoder policy; it matches a Lua source model using floor for positive bit coercion, but the original bit runtime/hardware coercion is not qualified. RGB/white helpers are representation APIs, without automatic product selection, new KOs or high-FP RF write authorization.

Validation: **527 native tests,34 XML/UI/source checks and7 executed ETS JavaScript tests pass**. Independently executing retained Lua contexts/formulas matched10 temperature results and8 lighting cases (lighting uses the stated bit-coercion model). Existing native SX1262 checks also pass and do not qualify SX1276 behavior. No ETS XML, parameter/KO layout or flash-format changes; versions remain application3.6/module0.2.0.

Final firmware validation passes for `develop_OpenKNX_XIAO_S3_SX1276_TP`, `release_OpenKNX_XIAO_S3_SX1276_TP` and `develop_OpenKNX_XIAO_S3_SX1276_IP`. The local dependency pin advances to `b55b272`. Builds do not establish SX1276 RF conformance, physical version3 interoperability, atomic flash recovery or real ETS migration. No firmware flashing or remote push was performed.
