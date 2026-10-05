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
