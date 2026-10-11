# RF policy, lab builds and battery diagnostics

Implemented software prototype, 2026-10-11. Release firmware keeps its existing
per-band duty limits. There is no RF quiet period after boot/reboot: commands
can transmit as soon as radio initialization and protocol checks finish.
The RAM-only accounting ledger starts fresh after reboot. See `iohc duty status`
for estimated eligibility delays when actual charged airtime exhausts the budget.

All develop/debug environments activate bypass by default without expiry, including IP and
standalone debug builds. Release environments reject it. The two existing bench
targets remain convenient aliases:

```
pio run -e bench_OpenKNX_XIAO_S3_SX1262_TP
pio run -e bench_OpenKNX_XIAO_S3_SX1276_TP
```

Debug builds require a shielded/conducted approved RF test setup. No activation
command is needed after startup. Use the console to inspect or disable bypass;
the confirmed on command re-enables it after manual off or a fault:

```
iohc duty debug on CONFIRM_SHIELDED_BENCH
iohc duty status
iohc duty debug off
iohc duty reset-debug
```

No ETS/NVS setting enables bypass. Debug web-console builds support the same
explicit confirmation command; KNX diagnostic KO commands cannot enable it.
All accepted airtime is still counted; off/reset-debug never refund it. Release
builds reject debug on. Faults and later identity changes disable it. Debug
reinitialization/reboot activates it again; there is no time-based expiry.
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
Status polls defer before enqueue/logging when quota prevents them.

Higher CH2 fairness and QualifiedPoliteAccess remain unavailable until complete
hardware/regulatory qualification. Current helper LBT is not sufficient evidence.

Details:
- [Module RF policy](../lib/OFM-IOHomeControl/docs/rf-access-policy.md)
- [Battery RF outcomes](../lib/OFM-IOHomeControl/docs/battery-rf-outcomes.md)
- [TODO status and hardware work](../lib/OFM-IOHomeControl/docs/rf-todo-progress-2026-10-11.md)
