# Raw light and bounded diagnostic integration

The OFM dependency is pinned to `4f78936daa3d527c75cb71f2fee0ae5f8c99640a`. Other dependencies retain their exact previous pins, including HardwareConfig `0c5a94d` on `v1`.

Sources, original attachment SHA-256 values, literal observations and privacy boundaries are committed in OFM `docs/light-followup-evidence.md`, `test/corpus/light-followup/` and the unchanged supplied fifteen-event JSON. Full local evidence and private originals are archived under `Velocet/Findings/2026-11-05-raw-light-and-bounded-diagnostics/`. Native application-body fixtures are kept separate from complete RF observations and synthetic authentication tests.

Local validation on 2026-11-05:

- 903 native tests passed with no failures. Full `make -C test run check-storage corpus` passed, including importer/privacy checks, production callbacks, storage and thirteen golden RF corpus tests.
- New light, empty-object, remote-group, window-selection, challenge-timing, pairing-channel and imported-observation cases passed in release and debug modes. The production window selector also passed MVS compiled/enabled/disabled, movement-mode and explicit-speed-conflict tests. Final native/build-mode checks were rerun after the last movement-selection correction.
- All three final pinned firmware builds succeeded: `release_OpenKNX_REG1_ESP_V00_11_SX1276_IP` (RAM 124204/327680), `develop_OpenKNX_XIAO_S3_SX1262_IP` (126352/327680), `release_OpenKNX_XIAO_S3_SX1276_TP` (116584/327680). REG1 static RAM is 40 bytes above the previous successful 124164-byte baseline, retaining substantial link headroom. Optional diagnostic rings/groups allocate only when enabled.
- Debug RF remains permanently unlimited as specified; production RF admission, identity and authentication tests passed. No firmware was flashed, no RF operation or motion was initiated and no commits were pushed. Successful baseline remote CI runs do not represent new remote CI for these local commits.

The raw sample has unit UNKNOWN and is exposed only through authenticated session diagnostics. Live 0x73 subscription remains withheld pending a qualified direct-reply authentication policy; the offline builder does not send. Lux/irradiance conversion, object-13 voltage/history semantics, physical garage latency, same-window travel and directed CH3 compatibility still require the hardware evidence listed in the OFM reports. No unqualified physical units, global preamble/timeout changes, heater writers, key reset or class2 object allowlist expansion were introduced.
