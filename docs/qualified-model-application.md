# Qualified heating model application

Application 4.10 / IOHomeControl module 0.10 adds an explicit unknown/AGILIA/Adelis model selector in reserved bits 4–3 of the existing three-byte heating block. Unknown is the default and existing channels require deliberate selection plus fresh live name qualification before writes. The selector is excluded from configuration transfer. Existing parameter sizes, offsets, KO addresses and DPTs remain unchanged; Adelis does not receive AGILIA window controls.

`python3 tools/check_heating_model_layout.py` compares all 3403 pre-existing generated macros against application baseline f275a26: only application/module versions change; four model macros are added. OFM's schema regression also checks the XML layout and model-specific UI. This establishes layout compatibility, not an automatic grant of previous heating permissions.

Source and implementation boundaries: [upstream source report](../../OFM-IOHomeControl/docs/upstream-alignment-sources.md) and [qualification gates](../../OFM-IOHomeControl/docs/upstream-alignment-validation.md). The exact committed OFM dependency is recorded in dependencies.txt; HardwareConfig stays on the working v1 pin.

OpenKNXproducer 4.3.12 successfully expanded the XML and regenerated include/knxprod.h. This Mac lacks the configured XSD and ETS, so no signed .knxprod was created or validated. Sensor and DHW measurement KOs, VELUX speed presets, physical testing and remote CI remain subject to the documented gates. The local review branches are not merged or pushed.
