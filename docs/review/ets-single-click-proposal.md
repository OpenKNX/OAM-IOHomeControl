# Proposed first-click ETS reconciliation

Not applied. Approval is needed because automatic approval review rejected removing
the explicit preview confirmation, citing persistent configuration side effects.

The adjacent patch replaces only the mandatory preview-token second-click return.
It retains generation/boot/revision checks, the freshly computed occupancy-bound
plan, identity-bound assignments, existing channel collision guards, parameter
readback and receipt handling. The next confirmed implementation step also needs
the first-click and second-click no-op ETS host tests updated and rerun. The patch
has not been validated as an applied implementation.

Expected effect: clicking “Ergebnis übernehmen” computes and applies the eligible
plan immediately. This can persist assignments on the first click. Existing
production code still requires the preview confirmation.
