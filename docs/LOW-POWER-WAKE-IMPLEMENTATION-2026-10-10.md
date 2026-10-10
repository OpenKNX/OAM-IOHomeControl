# Low-power wake todo implementation — 2026-10-10

The software changes and regression tests are in sibling `OFM-IOHomeControl`,
used here through `lib/OFM-IOHomeControl`. See
[policy, test procedure and remaining hardware work](../../OFM-IOHomeControl/docs/LOW-POWER-WAKE-2026-10-10.md).

The supplied gateway firmware was re-disassembled locally. The bounded evidence
is in [the call-site report](STM32-WAKE-CALLSITES-2026-10-10.json), reproduced with
`PYTHONPATH=/path/to/capstone python3 tools/inspect_stm32_wake_paths.py firmware_dump/io-homecontrol-stm32-20220823081517.bin`.
Shared 2W frame preparation clears LOW_POWER; the 1960-UART-byte prefix is not
proven for real PRIVATE 0x03 STARTs. No waveform/RX-duty-cycle measurements or
original actuator dump analysis have been performed. Default wake remains 1024.

`dependencies.txt` pins the local OFM implementation commit
`40042243051db9f6990c991c3774562e2d4188b1`. The commit has not been pushed;
use the sibling module checkout when reproducing these changes locally.
