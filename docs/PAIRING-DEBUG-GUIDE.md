# io-homecontrol Pairing And Debug Guide

This guide is for users who have real io-homecontrol hardware and want to pair devices with this gateway, or collect useful logs when pairing does not work.

For a short German version, see [PAIRING-DEBUG-GUIDE.de.md](PAIRING-DEBUG-GUIDE.de.md).

## Before You Start

Use a `develop_...` firmware build, not a `release_...` build. The develop builds provide the serial diagnostics that are needed for root-cause analysis.

Recommended preparation:

1. Flash the correct develop environment for your board.
2. Open a serial monitor at `115200` baud.
3. Make sure the target channel is configured in ETS:
   - set the correct device type
   - choose `2W` or `1W`
   - for `1W`, enter the known actuator node ID
4. Keep the device close to the gateway during pairing.

## 2W Pairing

Use this flow for normal bidirectional devices.

1. In ETS, open the target channel.
2. Set `Protokollmodus` to `2W`.
3. Set `Anlernmodus` to `Anlernen`.
4. Put the io-homecontrol device into its manufacturer-specific learn mode.
5. Trigger pairing:
   - preferred: ETS online pairing action for that channel
   - alternative: serial console command `iohc pair NN`
6. Wait for the pairing flow to finish.
   On a develop build, the serial console should immediately show `ETS: pairing started for channel N` when the ETS action is received.
7. Check whether the channel is paired:
   - ETS object `K9 Pairing-Status`
   - or serial console `iohc status NN`
8. If pairing succeeded, run one functional check such as `iohc send NN 50` for a position-capable device.

## 1W Pairing

Use this flow for unidirectional devices.

Important constraints:

- `1W` pairing is blind learn, so the actuator does not confirm success over the air.
- You must know the actuator node ID in advance.

Steps:

1. In ETS, set `Protokollmodus` to `1W`.
2. Enter the actuator node ID in `1W Aktor-Node-ID`.
3. Set `Anlernmodus` to `Anlernen`.
4. Put the actuator into learn mode.
5. Trigger pairing:
   - preferred: ETS online pairing action
   - alternative: serial console `iohc pair NN AABBCC`
6. Verify with a real device action, because a pure RF acknowledgment is not expected in the same way as `2W`.
   On a develop build, the serial console should immediately show `ETS: 1W pairing started for channel N` when the ETS action is received.

## Quick Health Check Before Pairing

Run these commands before blaming the device side:

1. `iohc status`
2. `iohc radio`
3. `iohc radio raw`
4. `iohc radio txtest`
5. `iohc radio sweep 3`

What good looks like:

- `iohc radio` should show `init=1`
- `iohc radio txtest` should report `done=1`
- `iohc radio sweep 3` should finish with `ok=...` and `timeout=0`

If those basic radio checks already fail, the pairing problem is probably below the protocol layer.

## If Pairing Does Not Work

Collect one complete log from boot to failure. Partial snippets are much less useful.

### Minimum Logging Sequence

After reboot, run these commands in order:

1. `iohc status`
2. `iohc radio`
3. `iohc radio raw`
4. `iohc pairdiag on`
5. Start pairing:
   - ETS online pairing action
   - or `iohc pair NN`
   - or `iohc pair NN AABBCC` for `1W`
6. Wait until the controller returns to idle or clearly fails.
7. `iohc status NN`
8. `iohc radio`

If the channel is still not paired, also run:

1. `iohc discover`
2. `iohc discover spe`
3. `iohc radio txtest`
4. `iohc radio sweep 3`

If there is nearby io-homecontrol traffic and you want extra RF context:

1. `iohc scan start`
2. wait 10 to 20 seconds
3. `iohc scan stop`
4. `iohc scan dump`
5. `iohc scan stats`

## Copy-Paste Command Blocks

Use the block that matches your hardware. Replace `NN` with your channel number. For `1W`, replace `AABBCC` with the actuator node ID.

### SX1262

```text
iohc status
iohc radio
iohc radio raw
iohc radio txtest
iohc radio sweep 3
iohc pairdiag on
iohc pair NN
iohc status NN
iohc radio
```

For `1W` on SX1262:

```text
iohc status
iohc radio
iohc radio raw
iohc radio txtest
iohc radio sweep 3
iohc pairdiag on
iohc pair NN AABBCC
iohc status NN
iohc radio
```

### SX1276

```text
iohc status
iohc radio
iohc radio raw
iohc radio txtest
iohc radio sweep 3
iohc pairdiag on
iohc pair NN
iohc status NN
iohc radio
```

For `1W` on SX1276:

```text
iohc status
iohc radio
iohc radio raw
iohc radio txtest
iohc radio sweep 3
iohc pairdiag on
iohc pair NN AABBCC
iohc status NN
iohc radio
```

If pairing still fails, append this extra capture block:

```text
iohc discover
iohc discover spe
iohc scan start
iohc scan stop
iohc scan dump
iohc scan stats
```

## What To Send Us

Please include all of the following:

1. Board and firmware environment, for example `develop_OpenKNX_XIAO_S3_SX1262_IP` or `develop_OpenKNX_REG1_ESP_V00_11_SX1276_TP`
2. Radio backend: `SX1262` or `SX1276`
3. Device type you tried to pair
4. Whether it was `2W` or `1W`
5. For `1W`, the actuator node ID you used
6. The exact console commands you ran
7. The full serial log from boot until after the failed attempt
8. Whether the physical device reacted at all
9. If available, a screenshot or exact text of the relevant ETS channel parameters

## What Helps Most During Root-Cause Analysis

These observations are especially useful:

1. `iohc radio txtest` passes, but pairing fails
   - local TX path is probably healthy; the issue is more likely discovery, learn mode, protocol, or authentication
2. `iohc radio sweep 3` passes, but `iohc discover` finds nothing
   - likely device-side learn-mode issue, frequency mismatch, or missing real traffic nearby
3. `iohc discover` sees devices, but `iohc pair` fails
   - RF receive path is probably working; the issue is likely in pairing/auth flow or device compatibility
4. `1W` pairing fails with no reaction
   - first check the actuator node ID; a wrong node ID makes blind pairing indistinguishable from RF failure

## Short Example Session

For a `2W` debug session on channel 1:

1. reboot device
2. `iohc status`
3. `iohc radio`
4. `iohc pairdiag on`
5. put actuator into learn mode
6. `iohc pair 01`
7. wait for logs to settle
8. `iohc status 01`
9. `iohc radio`
10. if not paired: `iohc discover`, then `iohc radio txtest`, then `iohc radio sweep 3`

That usually gives enough information to separate RF problems from pairing-flow problems.