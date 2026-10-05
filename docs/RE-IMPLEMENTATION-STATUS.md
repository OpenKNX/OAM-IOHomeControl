# Reverse-engineering implementation checkpoint — 2026-10-04

> **Current checkpoint — 2026-10-05:** [Authoritative twelve-point matrix](../../../IOHomeControl/docs/implementation/CURRENT-IMPLEMENTATION-STATUS.md). Older entries below are historical checkpoints.

OFM `cdeaa4a`, module 0.5.0; OAM application 3.9. All twelve points have software changes and separately recorded primary commits; the matrix identifies partial acceptance and remaining implementation. The four new recognition permissions are ETS-only and default to preserving manual settings. Channel memory/KO layout stays 68 bytes / 25 objects.

Validation: 558 native tests; 34 UI/source checks; 16 actual ETS JavaScript tests; 2 tuning-summary tests; recognition generation check; producer 4.3.12 integrity and project-20 XSD validation; SX1276 TP development, TP release and IP development builds all passed. Producer had no ETS installation, so no signed `.knxprod` was created. No hardware was flashed and no physical peer qualification was performed.

Remaining: global 2W journal power-cut qualification, actual ETS round trips, complete common commissioning UI/transaction coverage, exact commercial binding, operational product-specific KNX objects and physically qualified high-FP reads/writes. See the matrix for exact boundaries; compiled conversion/policy code does not enable RF writes.

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

## 2026-10-05 continuation: master framing, identity binding and high-FP qualification

Separate local OFM commits as Franz Reisenhofer:

| Commit | Scope |
| --- | --- |
| `dca1be6` | Controller3D preserves version3 from its authenticated working request; independent MAC/header tests |
| `db9c6b6` | Exact consistent identity evidence binds retained-source semantic families for diagnostics |
| `d26507d` | Product-bound RGB and FP14 activation representations with transactional output validation |
| `bbfe2a4` | Runtime `iohc 2wdiag version auto|3` and a real queued-controller authentication regression |
| `d83580c` | Physical SX1276/peer/version3/high-FP bench procedure and explicit unrun status |

The original STM32 MasterSession calls the generic continuation copier at0x0800EB9C when building3D (0x0800F09A/0x0800F150). Copier0x0800EC00–0x0800EC1C inserts/removes the extension to match its source working frame. Production authentication now preserves that form. This bounded change does not adopt all copied flags: ordinary request versions0/1/2 retain the established outgoing version0, and controller START/END, LOW_POWER and ACK policy retain their existing continuation values. The HMAC remains original CMD+DATA. The bench override is applied once to each newly built queued2W request; retries/authentication retain it even if the control changes later. It does not choose version for separate pairing/discovery state machines, negotiate a persistent per-peer preference, modify ETS or affect1W. `auto`/`reset` clears the override for subsequent requests. Extended payload overflow still fails serialization before transmission.

Family binding requires valid full actuator metadata, no manufacturer signature conflict and no available GI2 profile/subprofile disagreement. RGB binds exact6/1 for manufacturers0/2; white exact6/2 for manufacturer2, scoped to retained definitions. Atlantic manufacturer12, exact22/1 plus GI2[7..9]=620000 or520001 binds PassAPC heat-pump/hybrid families. The source excludes Atlantic from the generic public MP/FP15/16 generator path: **PassAPC binding must not select the normalized generic HeatPump codec**. Names and manual/expert settings are not changed. Database generation/variant bits, exact commercial models and temperature bounds acquisition remain unresolved.

Product-bound lighting builders produce only MP/FPI representations, without originator/ACEI, RF header, authentication, CRC or enqueue. They reject wrong family, conflicting evidence, invalid color/Kelvin, unknown white MP sentinels and insufficient capacity without changing buffer/length. RGB255,0,0 yields000000607CA9654C; safe blackC8000000; white4250K with raw ignored MP yieldsD40000046400. Lighting truncation/black policies still need original runtime/peer comparison. The existing RF FP1–3 diagnostic gate remains effective; no arbitrary FP10/11/14 writer or new KOs are enabled.

Software checks: **531 native,34 XML/UI/source and7 actual ETS JavaScript tests pass**, plus the existing native SX1262 suites. These include ordinary/extended controller MAC equivalence, an ordinary received challenge answered in the explicitly selected extended working form, identity negatives and atomic representation output failures. Physical testing remains unexecuted: only Bluetooth/debug-console serial ports were found, with no identified SX1276 board/peer. `OFM/docs/SX1276-PEER-QUALIFICATION.md` records the concrete bench sequence and acceptance evidence needed. No radio measurements, original-peer version3 acceptance, commercial model binding, signed ETS product or flash power-cut result is claimed. No parameter/KO/flash-layout change; application/module remain3.6/0.2.0.

Final firmware checks pass for SX1276 TP-development, TP-release and IP-development with the runtime bench control included. The dependency pin advances to`d83580c`. Physical checks remain pending hardware/peer access; generated build metadata is excluded from this commit.

## Implementation continuation — 2026-10-05 (module 0.4.0 / application 3.8)

These are software implementations of recovered layouts, not new binary discoveries or physical qualification.

- `4a7d645`: checked ESP32 `iohcnet` journal commits controller node, global 2W key and sixteen channel bindings together. Two 348-byte records carry version, generation, CRC and exact readback. Corrupt nonempty records or failed commits block 2W transmission. Pairing/import commit bindings before advertising success; unpair commits tombstones. Legacy OpenKNX metadata remains a separate mirror. Power-cut/wear tests and checked backends for other MCUs remain open.
- `4efa524`: boot identity, generation, frozen snapshot revision, bounded pairing/import host jobs and error reason; ETS imports use these tokens for candidate reads/assignment and cancellation. Pairing budget is 120 seconds; import budget 360 seconds. These are host workflow limits, not recovered RF/RCM timings. Receipt resume retains manual settings. Full common console/ETS transaction coverage and actual ETS download tests remain open.
- `d105ebd`: volatile identity/key-bound MP/FP observations record freshness, transaction generation and trust. Existing correlated private responses and FP1–FP3 diagnostics populate observations. Correlation is not authentication; coherent RGB/white conversion still requires authenticated evidence. No new high-FP RF request layout or product KNX publication is enabled.
- `3d93555`: queued priority `19/1A` reads validate three-byte responses, retain the unnamed byte, decode the 30-second timer and originator, and skip refresh for raw `FF`. Refresh rereads use recovered seconds + 20. Sensor `84/85` reads validate six-byte responses and supported scale codes; physical units remain unknown. The exact 17-byte sensor-information decoder does not authorize guessed subscription requests.
- `cacf3b9`: bounded, peer/token-bound segmented object-transfer model for `46/47`, `48/49`, `4A/4B`; 1024-byte capacity, 18-byte chunks, low-seven-bit sequencing, disposition/abort handling, fixed-provider alignment, cancellation and deadlines. Transport words remain caller-supplied and opaque. This model is not connected to the RF queue; object business schemas and authenticated transaction integration remain open.
- `5cfe0d1`: receipt reads/ACKs require matching live key and committed binding; legacy batch import rejects same-node/different-key conflicts. `fdad9b2` versions the additive interface as module 0.4.0.

Online function-property object 160/property 10 additions: `23` capabilities/boot identity (10-byte reply); `24` extended job (26); `25` frozen import candidate (20); `26` token-bound assignment; `27` boot/generation cancellation; `28` raw product observation (20); `29` correlated priority sample (15); `2A` correlated sensor status (17). All multibyte token/generation/age fields are BE32; profile remains LE16. Private keys are never returned. Old commands remain available for older firmware; frozen assignment fails on stale/rebooted tokens.

ETS adds a global commissioning-cancel button. Channel parameter memory remains 68 bytes and channel KOs remain 25 objects. Product-specific KNX objects, sensor subscriptions, full RF object-transfer integration, exact commercial/generation binding and qualified high-FP writes are still missing. Unknown schemas (`4300`, `8100/8103`, `A607`, unnamed `6F`/`73` fields, GI1 byte11, FP4–FP7/timer meanings, Atlantic FP13) are not assigned invented meanings.

Validation: 551 native tests, 34 UI/source checks, 13 actual ETS JavaScript tests, 2 tuning-summary tests and recognition generator check passed. Producer integrity and project-20 XSD checks passed. ETS is unavailable, so no signed product or real ETS round trip was produced. No physical peer, SX1276 measurement or power-cut result is claimed.

Final production validation: SX1276 TP development, TP release and IP development all passed against OFM `f801e10`, application 3.8/module 0.4.0. Generated header differs only in the application/module version constants, preserving repository line endings.


## Further implementation — 2026-10-05 (module 0.5.0 / application 3.9)

This checkpoint implements existing recovered findings; it adds no physical-peer acceptance claim.

- **`cd28257` — Sensor-information read and management identity binding.** `iohc sensor info NODE` queues only the recovered `8B FF` read form for a paired 2W node with valid Sensor-class identity. The exchange accepts `8C` only with at least 17 data bytes, decodes/retains the 17-byte prefix and exposes it through function-property **`2B channel`**. The 26-byte reply is result/schema/channel/valid at 0..3, age BE32 at 4..7, raw response bytes at 8..24, trust at 25 (`2` correlated, `0` absent). No 17-byte subscription WRITE, auto-subscription, physical-unit inference or sensor KNX publication is enabled. Priority/status/information reads snapshot the channel key; identity/key changes reject pending TX/replies, hide old samples and stop old priority refreshes. This is request correlation, not proof of authenticated sensor state.
- **`ca9bb9e` — Additional product codecs.** Strict heating-level decoding accepts only the eight recovered `FCxx` values; unknown input cannot fall back to off. Separate Heat Pump and Atlantic DHW FP15/16 codecs preserve raw capabilities, uninterpreted bits and differing two-bit meanings. In particular Heat Pump `00/11` remain unnamed, Atlantic `00/11` mean Keep_Current/Not_Used, and Atlantic's common `4000` remains uninterpreted. Atlantic FP10 rate management is a separate enum. IndoorSiren FP9..14 codecs pack three duration/options pairs and zero unused sequence slots. Numeric duration is 100..204600 ms, rounded to 100-ms units; `0` is the default pattern (duty must be zero), `7FF` default duration, and repetition `3FF` unlimited. Reserved volume/visual codes remain visible on decode and cannot be encoded. Duty conversion follows retained `scaleChange`'s one-decimal rounding, then explicit positive truncation before the modeled bit shift; original runtime fractional coercion and on-air behavior remain unqualified. These are explicit-product offline codecs/representations, not automatic commercial bindings or RF producers.
- **`0476f95` — Read-only ETS evidence views.** Global **Einrichtungsstatus lesen** displays job owner/stage/error, generation, revision and candidates. Per-channel **Erkennung / manuelle Vorgaben / Produktevidenz lesen** displays current profile/manufacturer evidence, manual override and recognition permissions, family-binding limits, and raw RGB/white observation trust/generation/age. It checks the channel node again before displaying the result, preserves every ETS setting and sends no RF query. It shows current evidence, not a stored per-field history; no ACK/download-success claim is made.
- **`928f24d` — Journal recovery hardening.** Generation zero is invalid; two valid, different records with equal generations are corrupt rather than arbitrarily selecting a key/binding state. Native tests cover all **349 cut positions** of a 348-byte replacement record. Empty interrupted target leaves the old complete state; partial nonempty records fail closed; a full durable record with a lost write acknowledgement loads the new complete state after simulated restart, while the original commit still returns failure. This is a conservative record fault model, not an ESP32 NVS or physical power-cut experiment.
- **`cdeaa4a`** versions the ETS interface as OFM 0.5.0. OAM application 3.9 encodes version 57, module version 5. Channel parameter memory and KOs remain **68 bytes / 25 objects**.

Offline diagnostics: `iohc codec heating RAW16`; `iohc codec modes heatpump|atlantic-dhw FP15 FP16`; `iohc codec siren SOUND16 OPTIONS16`. These do not enqueue RF packets. Product selection is explicit and must not be interpreted as discovery of a commercial model.

Validation: **558 native tests**, **34 UI/source checks**, **16 actual ETS JavaScript tests**, **2 radio-trial summarizer tests**, and recognition generator check passed. Producer integrity/project-20 XSD validation passed; no ETS installation means no signed `.knxprod` or real ETS import/download test. Final production build/integration results follow below.

Still open: physical SX1276/peer and power-cut qualification; exact commercial/generation discriminators; authenticated high-FP read/coherent-tuple production and qualified writes; product-specific KNX object sets/publication; actual subscription writes and monitoring policy; RF integration of segmented object transfers and unresolved object schemas; full common commissioning transactions and persistent per-field evidence history. High-FP RF write permissions remain disabled.

Final production validation: all three SX1276 TP development / TP release / IP development builds passed against OFM `cdeaa4a`. Header generation changed only application/module version constants (57/5), preserving repository line endings.
