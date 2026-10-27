## Application 4.9: debug RF bench admission — 2026-10-27

- Pin OFM `d9709cc34f66ca7012835ee5a55170a623b7b558` so the version 4.9 debug bypass is included in dependency-based builds.

- Default OPENKNX_DEBUG builds to bypass software duty, CCA/LBT, TX quota and read-only diagnostic RF admission limits for shielded bench testing. Retain airtime accounting, diagnostic logging, protocol timeouts, authentication and identity-collision protection.
- Preserve release RF admission behavior. Add debug/release regression coverage and correct debug tracking logger compilation.
- Advance ETS application version to 4.9 (encoded 73); preserve parameter/KO layouts and flash schema 18.

## Application 4.8: dual-controller RF evidence — 2026-10-27

- Pin OFM `3b5ba09a41c76ab5db96ea70b87d7fd34775afae`. Preserve qualified immutable first collision evidence, separate local duty/CCA denial from actual peer silence and authenticated verification, and expose read-only ETS outcomes.
- Add bounded volatile background-poll pause, explicit SPE/standard diagnostic scans, receive-window/filter provenance and independent status transport/last-commander attribution. Preserve foreign-status ownership guards and all RF admission safeguards.
- Add source-attributed 64/61/52-second payload excerpts, synthetic transport regressions, full-trace speed comparison and sanitized local peer-configuration tools. Credit laberning/home_io_control; original seven field logs and real high-byte/target-change captures remain unavailable.
- Preserve current application/ETS 4.8 and flash schema 18. Reduce the classic ESP32 IP volatile trace ring to 14 slots for static DRAM headroom; other release targets retain 24. Physical A/B/C, ETS-host and radio qualification remain unrun. See `lib/OFM-IOHomeControl/docs/DUAL-CONTROLLER-DIAGNOSTICS.md` and `docs/dual-controller-validation-2026-10-27.json`.

## Application 4.7: remaining time and moving-poll recovery — 2026-10-27

- Pin OFM `e48a53cc007a927d0a6877b15e4d1213302729e3`. Decode full 16-bit remaining seconds only for owned, correlated native 03/04 main-info polls. Exclude ACK/tilt/probe layouts, short/foreign/mismatched replies and untracked timing updates.
- Preserve measured current/target and reported STOPPED/moving state. Keep normal cadence for unavailable countdowns only inside an existing epoch. Distinguish positive/zero/unbounded/undefined counts; shorten existing follow-up only, retain the low-power 10 s floor, bounded deadline and identity/epoch resets.
- Keep normal cadence for two trusted moving single-attempt poll misses, then use existing auth/silence backoff. Local admission/driver failures defer fairly without consuming peer misses or extending tracking. Preserve STOP-settle exchange budgets and RF duty/CCA admission.
- Add negative mutations and a reproducible per-frame corpus audit. All 177 original YAML hashes stay pinned to c82d38f; synthetic 256-second vectors are not captured high-byte proof. Credit laberning #184 `821454537355a1d20f8f8622889611f4f491a11b`; native offsets remain distinct from KLF/Overkiz API semantics.
- Preserve application/ETS 4.7 and flash schema 18. Validation: `docs/remaining-time-validation-2026-10-27.json`. Hardware/ETS/storage/spectrum qualification remains unrun; release acceptance is false.

## Application 4.7: three-shutter diagnostics — 2026-10-27

- Pin OFM `f9834597b0690c5c9316292d6d1962d25ffd6311`. Add bounded per-node passive/active/directed/flash evidence, session/build identity, candidate decisions and a read-only summary. Preserve evidence after import finalization.
- Add explicit existing-key `iohc keyimport scan` and targeted `verify NODE` operations. Use the existing scheduler with strict duty/CCA admission and matching committed identity; do not extract keys, re-pair or write membership/configuration.
- Add filtered incremental RF observations with overwrite counts, foreign-destination/authentication labels, optional config history and guarded last-controller diagnostics. Redact import challenge/HMAC material.
- Require ETS parameter readback before assignment ACK, log result/channel decisions, report project activation to volatile diagnostics, and avoid repeated receipt writes. The existing preview confirmation remains; first-click completion awaits approval after automatic review rejected its removal.
- Preserve flash schema 18 and application/ETS 4.7. Procedure: `lib/OFM-IOHomeControl/docs/THREE-SHUTTER-DIAGNOSTICS.md`. Validation: `docs/three-shutter-validation-2026-10-27.json`; hardware/ETS-host acceptance remains unrun.

## Application 4.7: original laberning capture regressions — 2026-10-27

- Pin OFM `72dedab8da41cb8c49c9b0491ef848c55dff4af9`. Import 160 missing original YAMLs from laberning `c82d38f47901b71c1c63413e638241dbe1aa2d06`, reusing 17 identical existing files. Preserve original bytes, MIT attribution, Git blob/SHA-256 provenance, radio labels, redactions and reconstructed/synthetic evidence limits.
- Validate all 1,104 source frames on the host; parse 897 bounded native vectors and cross-check 43 public rekeyed HMAC cases. Add source/security checks, targeted controller/KNX callback regressions, and negative mutation tests to CI. Raw YAML and long observer data stay outside firmware.
- Fix two capture-proven status issues: honor a reported moving state near target, and end stopped-status tracking without snapping measured current or overwriting a distinct reported target. Protect MOTO refusals, stale position/tilt ACKs, sensor priority, foreign status, pending discovery ownership, preamble and optional pairing behavior.
- Preserve application 4.7, HTG/HAW and all parameter/KO offsets. Record builds, runtime module hashes and DRAM evidence in `docs/original-captures-validation-2026-10-27.json`; corpus results do not qualify hardware or set release acceptance.

## Application 4.7: inbound status replies — 2026-10-26

- Pin OFM `ee82fb974d4ecc5f4aae9905eeecca3827d04b11`. Paired, directed 2W status now has a distinct identity/key/session-bound inbound challenge context. Its saved payload stays untrusted until the matching 0x3D HMAC verifies.
- Give the generated 0x3C and at most one authenticated same-frequency 0x72 a bounded immediate reply. Retain all three ACK copies and wire flags; remaining copies use ordinary admission. Receive-channel-first ordering is an implementation policy awaiting real peer captures and release qualification.
- Bind reply grants to explicit producer roles, expected state/opcode, channel identity and the original 25 ms timestamp. Raw frames, rekeying, cancellation, expiry and radio faults cannot reuse them. Scope busy CCA counters to their candidate and retain per-band accepted-TX accounting.
- Add inbound security/timing/CCA regressions and permanent mutation checks to the standard native suite. Preserve ETS application 4.7 and all object/parameter layouts; retain the classic ESP32 IP 16-entry diagnostic ring.
- Validation, firmware hashes and before/after static DRAM are recorded in `docs/inbound-status-validation-2026-10-26.json`. Real SX1276/SX1262 timing, ACK copy/channel captures and spectrum-access qualification remain `not_run`; no firmware was flashed.

## Application 4.7: 2W admission and status recovery — 2026-10-26

- Pin OFM `93ba0a69e49450db5dd87eaf636323eeba62a6d5`. 2W in-session authentication responses are no longer delayed by additional LBT; START transmission access policy centralized. Only peer/session/frequency-bound replies qualify; carrier sensing never falls through to an unchecked send on busy or invalid RSSI.
- Retry failed tracked status reads after 5 seconds, then progressively back off to 300 seconds. Preserve the low-power minimum, fixed ten-minute window, STOP settling and per-band duty budget. Bind failures to the owning channel and key revision; queued/unsent reads and unrelated responses do not change peer streaks or fabricate status.
- Laberning #178/#179/#180 inform the fixes; Velocet supplies protocol consistency, not the application retry ladder or spectrum-access qualification.
- Keep ETS application 4.7, HTG/HAW banks and parameter/KO offsets unchanged. Use a 16-entry diagnostic trace ring only for classic ESP32 IP release to fit the current dependency set's static DRAM budget; the default remains 24.
- Record native, build, firmware hash and RAM evidence in `docs/two-way-recovery-validation-2026-10-26.json`. Physical RF/peer, spectrum-access, storage and ETS qualification remain `not_run`; no firmware was flashed.

## Application 4.7: Atlantic recovery and Home/Away — 2026-10-22

- Pin OFM `0ec3ace` (discovery `fdebd28`, Home/Away `52c210e`, qualification gates `22117eb`, standard test integration `0ec3ace`). Reference: Laberning `b4b749353cfaa586868926e84d953eff6db4ff13` (#176); keep public masked cryptography absent and synthetic security proofs separate.
- Make the normal explicit Atlantic workflow search all three frequencies in two bounded passes after a silent direct probe. Verify discovered heater addresses independently, then require explicit durable assignment. Add ETS start/status/assignment buttons, multiple-responder tests, strict LBT/quota handling and RX restoration before RSSI reads.
- Add qualified AGILIA IO Home/Away commands through the normal KNX path. Default-off model confirmation, exact challenged ACKs, unknown startup, no write replay and separate command/status objects prevent ACKs from appearing as measured occupancy or heating effect. Keep 0101 separate and 012A diagnostic/read-only.
- Append 48 HAW KOs at 1960; preserve all 2187 checked application 4.6 constants, 14733 parameter bytes, HTG stride 10 and the 580-byte heating cache. See README for upgrade and group-association checks.
- Verified native protocol/controller/exchange (420/275/73) with both radio configurations, production adapters, storage, UI (55), ETS JavaScript (57), evidence/fixture integrity (7), producer integrity/XSD and all 16 expanded channel trees. All four release firmware targets and the SX1276 bench target build; REG1 IP retains 1176 bytes of DRAM segment margin.
- Physical RF/heater behavior, 30-minute AUTO effects, power-cut testing, real ETS migration/downloads and signed export remain unrun release gates. No firmware was flashed. Reproducible commands and results are recorded in `docs/atlantic176-validation-2026-10-22.json`.

## REG1 IP release memory fix — 2026-10-21

- Fix workflow run 39639124329: both pinned and branch builds exceeded the classic ESP32 DRAM linker segment by 104 bytes in `release_OpenKNX_REG1_ESP_V00_11_SX1276_IP`.
- Pin OFM `0c15cac`. Compact heating cache field padding and share its immutable invalid-channel view in flash. Reduce module BSS by 1400 bytes while preserving all 16 channels, full raw replies, polling and pairing behavior. Add cache-size and maximum-raw-reply/unknown-state regression checks.
- Verified all four release targets from `scripts/Build-Release.ps1`, including REG1 IP with 1296 bytes of DRAM-segment margin. Full native, storage, UI and ETS JavaScript checks pass; parameter/KO layout is unchanged.

## Pairing recovery and Atlantic advice — 2026-10-21

- Pin OFM `466804f` (recovery commit `fa8dcec`, Atlantic advice commit `466804f`). Recover a missing 0x33 in normal 2W push pairing through a bounded challenged name read before repeating key-init. Reject unchallenged, foreign, late, malformed or failed exchanges; require successful durable assignment. Report read acceptance separately from locally verified peer MACs.
- Recognize Atlantic manufacturer 12 / profile 1023/0 during normal pairing and discovery. Offer the explicit pull workflow in logs and ETS status; stop normal pairing before key push and preserve channel metadata, assignments and keys. Advice expires after three minutes and never starts acquisition or assignment automatically.
- Keep application 4.6 parameter/KO layout unchanged. Update ETS state labels and add a backward-compatible advisory tail to the status response. Validate native, production adapter, ETS JavaScript, schema/layout and both radio builds. Physical lost-confirmation and Atlantic RF tests remain pending.

## Application 4.6: guarded Atlantic heating — 2026-10-21

- Pin OFM `e31b8e5`. Add typed private register reads/writes, strict challenged response correlation, independent write readback and measured feedback with validity/provenance. Sensor register 010E is read-only; detection enable uses 0106. Other heating profiles keep their existing semantics.
- Add explicit staged Atlantic pull, bounded missing-proof retries, read-only +1 verification before keyed roll-call, and durable assignment to a chosen empty channel. Per-channel keys remain isolated from the global system key; restart recovery restores verified metadata.
- Append 160 optional heating KOs at 1800 (ten per channel), default-off polling and profile-qualified ETS controls. Preserve all 174 checked legacy layout constants, including 68-byte parameter blocks and 25 legacy KOs per channel.
- Migration: back up ETS first; remove legacy Kn+24 window writes, check Kn+22 DPT 5.010 mode links and Kn+21 setpoint feedback. Presence Kn+23 stays reserved. Online recognition and application download are required for qualified controls.
- Integrate seven pinned public capture fixtures; keep masked cryptography absent and synthetic proof tests separate. Validate native protocol/controller/exchange (416/263/67), storage, production publication/recovery, UI (53), ETS JavaScript (52), producer integrity/XSD and expanded channel layout. SX1262 release and SX1276 develop TP firmware builds pass.
- Physical Atlantic RF acceptance, further product-family qualification and signed ETS export remain unverified. No firmware was flashed.

## Application 4.5: pairing and garage compatibility — 2026-10-18

- Pin OFM `db31fce`: contextual FE errors and definitive key refusal handling; transcript-verified pull diagnosis with no automatic push or key persistence; garage MAIN-only EXECUTE and explicit MOTO1000 endpoint restriction; rejected optimistic-position rollback.
- Integrate 26 public Atlantic, MOTO1000, Nina, Sunilus, RS100 and Oximo protocol frames in the executable OFM corpus. Partial transcripts, masked authentication, missing physical CRC and synthetic proof/PHY tests are identified in the provenance.
- Increase ETS ApplicationVersion from 4.4 to 4.5 and regenerate the header for the default-off MOTO1000 option using unused byte 0 / BitOffset 6. Existing parameter offsets, 68-byte channel blocks and communication objects are unchanged.
- Verified native protocol/controller/exchange (410/245/65), radio, storage, UI (52), ETS JavaScript (51), production callback checks, producer integrity and 16 expanded channel trees. Both XIAO S3 SX1262 and SX1276 TP develop firmware targets build successfully.
- Physical device qualification, Nina authenticated responder, lost-33 proof design and the proposed full per-attempt telemetry counters require further implementation or hardware evidence. No physical RF test or signed ETS export is claimed.

## ETS channel setup and help — 2026-10-05

- Fix the automatic import-target range, internal JavaScript helper warnings and unsupported ETS help link in the linked OFM-IOHomeControl module.
- Nest product functions inside each enabled channel using prefix-scoped %TT% references and deferred channel substitution; module numbers are not hardcoded in the UI.
- Separate Expertenoptionen (protocol overrides and recognition controls) from Diagnose, grouped into status/recognition, sensors/priorities, metadata reads and product values.
- New channels allow supported 2W recognition by default. Status / Erkennung lesen adopts known functions while respecting manual opt-outs and profile overrides; an application download remains necessary.
- Add 47 concise German help topics and contextual help for every visible io-homecontrol setting. Preserve parameter memory and communication-object numbers.
- Verified: 39 channel UI tests, 34 ETS JavaScript tests, recognition/semantics generator checks, all 16 expanded channel trees and help archive coverage. A temporary ModuleType renumbering test verifies that product references follow the owning module while offsets and KO numbers stay unchanged. Producer 4.3.12 integrity checks pass without warnings. The staged standard and renumbered variants also pass XSD validation. ETS export and visual ETS acceptance remain to be checked on an ETS-equipped machine.
- Pin OFM-IOHomeControl 8b16922 for the matching channel templates, help and ETS scripts.

## OFM 0.5.1 integration — 2026-10-05

- Pin OFM `8ab63c0`; ETS application 3.9, parameter memory and KO layout remain unchanged.
- Add explicit allowlisted metadata object reads with challenged opening, automatic countdown/chunks and zero closure; completed raw readback is boot/token/key bound.
- Bound waits despite persistent preamble detection and prevent gateway/radio diagnostic ownership overlap.
- Read bytes are correlated, not authenticated product state. No object/high-FP RF writer or product KNX publication is enabled.
- Native suite: 563 passed; UI checks 34, ETS JavaScript 16, tuning-summary checks 2; recognition check passed.

## Application 3.9 / OFM 0.5.0 — 2026-10-05

- Pin OFM `cdeaa4a`; application/module version constants become 57/5 with unchanged channel memory and KOs.
- Add read-only global commissioning status and channel evidence views; manual settings are preserved.
- OFM adds sensor-information query, request-key-bound management observations, strict heating/siren codecs and ambiguous-journal rejection.
- Product KOs, subscription writes and physical high-FP/peer/power-cut qualification remain open.
- Validated: 558 native tests, 34 UI/source checks, 16 ETS JavaScript tests, producer/XSD and all three SX1276 builds.

## Application 3.8 / OFM 0.4.0 — 2026-10-05

- Require OFM `f801e10`; regenerate application/module versions without changing channel memory or KO layout.
- Add boot/revision-bound ETS import and global commissioning cancellation.
- Checked global 2W identity journal, observation provenance, priority/sensor reads and bounded object-transfer model are provided by OFM.
- No product-specific KNX KOs or high-FP RF writes are enabled. Hardware, power-cut and real ETS acceptance remain open.

# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

> **Note:** The version scheme deviates from [Semantic Versioning](https://semver.org/).
> This is required by technical limitations of the ETS: every change to the ETS
> application requires a bump of the minor version. The major version is constrained
> by the version space, which provides only 1 byte for major.minor (4 bits each).

## [Unreleased]

- Add checked ESP32 NVS 1W reservations, identity-preserving recovery and explicit failure diagnostics.
- Share generated recognition presentation with ETS; preserve manual settings through individual adoption permissions.
- Add commissioning job generations, resumable assignment receipts and distinct product-family/quantity/permission metadata.
- Capture SX1276 RX failure evidence and add controlled runtime bandwidth trials with evidence-based summaries.
- Bump ETS application to 3.7 and IOHC module to 0.3.0; retain channel memory and KO layout. Physical peer/high-FP write qualification remains open.

- Preserve controller authentication's extended working-request form; add runtime-only queued-2W version3 bench selection without automatic negotiation.
- Bind retained-source lighting and Atlantic PassAPC families using exact consistent identity evidence; keep commercial variants and expert settings separate.
- Add product-bound sorted RGB/FP14 activation representations and physical qualification procedure; high-FP RF transmission remains gated.

- Apply recovered recipient reply normalization to version-3 key extraction, including ACK direction, PRIORITY/BEACON and command-specific END rules.
- Add explicit product temperature conversions and an offline diagnostic console; reject unknown words, absent bounds and unsafe inverses.
- Add reference RGB and FP14 tunable-white conversion helpers with safe black handling; retain product/write qualification gates.

- Fixed wrapped-key log redaction for extended version-3 frame headers, including malformed-extension handling.

- Fixed 1W sequence-window reservations being silently suppressed by the shared flash write throttle; pause RF state machines while KNX configuration prevents persistence.
- Added product-scoped OVPd projection and window-lock read semantics, strict window-security enums and diagnostic provenance without enabling new writes or KOs.

- Composed ETS application 3.6 with OFM-IOHomeControl 0.2.0; retained existing parameter offsets and object numbers.
- Added recognition after normal 2W pairing with an explicit ETS type-adoption action, while preserving names and manual/expert overrides during recognition and import.
- Fixed extended version-3 headers and declared frame length overflow; added sorted sparse MP/FP representation with strict bounds.
- Clarified SX1276 FSK preamble byte units and remaining hardware qualification gates; retained existing radio settings.

- Fixed the ETS 2W key-extraction action freezing the commissioning dialog by replacing its synchronous polling loop with non-blocking, repeat-to-refresh steps.
- Fixed directed 2W communication with always-alive devices by resolving START preambles from the effective per-device power class; unknown devices now default to always-alive.
- Added discovery-based 2W power-class learning with flash persistence, an ETS `Automatic / Always Alive / Low Power` override, SPE roll-call and directed pairing preamble handling, status diagnostics, and runtime-only bench overrides.
- Aligned io-homecontrol channel selection with the current OpenKNX layout and added the shared per-channel suspension radio control.
- Added a configurable 1W enrollment finalizer with a conservative automatic VELUX/KLI profile.
- Serialized VELUX REMOVE, multicast ADD, STOP, and DOWN enrollment phases with deterministic timing, continuous logical sequences, failure diagnostics, and an in-memory phase trace.
- Added native regression coverage and source-derived masked KLI reference data; physical KUX/KLI and SX1276/SX1262 validation remains a documented bench step.
- Hardened 2W pairing response correlation and kept unicast response waits on their request channel.
- Defaulted 1W enrollment to `remove-add` (`0x39 -> 0x30`); `announce-add` remains an explicit diagnostic fallback.
- Documented the class-addressed 1W model and safe handling of extracted keys.
- Added documented pairing outcomes/diagnostics, RS100 silent-operation support, and repeatable native OFM suite entry points.

## v0.1.0: 2026-06-24 (Initial assembly)

- Initial assembly of the OAM-IOHomeControl application
- Build targets for XIAO ESP32-S3 and REG1 ESP DevBoard with SX1262/SX1276 radios and KNX TP/IP
- Integration of OFM-IOHomeControl, OFM-LogicModule, OFM-FunctionBlocks, OFM-Network and OFM-ConfigTransfer
