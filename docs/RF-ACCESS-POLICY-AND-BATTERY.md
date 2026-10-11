# RF policy, lab builds and battery diagnostics

Implemented software prototype, 2026-10-11. Ordinary firmware keeps its existing
per-band duty limits. Production boot/reboot has a conservative **3636000 ms
RF quiet period** to cover unknown prior airtime. RX is available during it.
See `iohc duty status` for recovery and estimated eligibility delays.

All develop/debug environments expose the temporary bypass, including IP and
standalone debug builds. Release environments reject it. The two existing bench
targets remain convenient aliases:

```
pio run -e bench_OpenKNX_XIAO_S3_SX1262_TP
pio run -e bench_OpenKNX_XIAO_S3_SX1276_TP
```

These require a shielded/conducted approved RF test setup. They start in normal
mode; a serial or debug web-console command can request a five-minute budget bypass:

```
iohc duty debug on CONFIRM_SHIELDED_BENCH
iohc duty status
iohc duty debug off
iohc duty reset-debug
```

No ETS/NVS setting enables bypass. Debug web-console builds support the same
explicit confirmation command; KNX diagnostic KO commands cannot enable it.
All accepted airtime is still counted; off/reset-debug never refund it. Release
builds reject debug on. Fault, identity change, expiry or restart disables it.
Never distribute bench images for normal field operation.

For explicit battery trials, enable Extended battery diagnostics for a paired
2W channel. Cyclic ETS status polling may remain disabled:

```
iohc battery 1 probe
iohc battery 1 probe09
iohc battery 1 objects
iohc battery 1 status
```

Submitted/queued is not RF success. Watch RF-start/completion/reply and terminal
results. No accepted TX => not_transmitted_duty_budget; partially sent exchange
=> exchange_duty_budget. Diagnostics show airtime/remaining quota/retry delay,
per-object results and historical evidence ages. Percent remains unknown.
Status polls defer before enqueue/logging when quota/recovery prevents them.

Higher CH2 fairness and QualifiedPoliteAccess remain unavailable until complete
hardware/regulatory qualification. Current helper LBT is not sufficient evidence.

Details:
- [Module RF policy](../lib/OFM-IOHomeControl/docs/rf-access-policy.md)
- [Battery RF outcomes](../lib/OFM-IOHomeControl/docs/battery-rf-outcomes.md)
- [TODO status and hardware work](../lib/OFM-IOHomeControl/docs/rf-todo-progress-2026-10-11.md)
