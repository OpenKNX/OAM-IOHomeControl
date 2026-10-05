#!/usr/bin/env python3
"""Verify the expanded ETS channel tree after running producer with --Debug."""
from pathlib import Path
import argparse
import re
import xml.etree.ElementTree as ET
import zipfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--project-root', type=Path, default=Path(__file__).resolve().parents[1])
ROOT = parser.parse_args().project_root
NS = {"k": "http://knx.org/xml/project/20"}
tree = ET.parse(ROOT / "src/IoHomecontrol.debug.xml")
parents = {child: parent for parent in tree.iter() for child in parent}
parameters = {p.get("Id"): p for p in tree.findall(".//k:Static//k:Parameter", NS)}
refs = {p.get("Id"): p.get("RefId") for p in tree.findall(".//k:Static//k:ParameterRef", NS)}
objects = {o.get("Id"): o for o in tree.findall(".//k:Static//k:ComObject", NS)}
object_refs = {o.get("Id"): o.get("RefId") for o in tree.findall(".//k:Static//k:ComObjectRef", NS)}
dynamic = tree.find(".//k:Dynamic", NS)
pages = [p for p in dynamic.findall(".//k:ParameterBlock", NS)
         if re.fullmatch(r"IOHC_IOHCChannel\d+Page", p.get("Name", ""))]
assert len(pages) == 16, len(pages)
for page in pages:
    channel = int(re.search(r"Channel(\d+)Page", page.get("Name"))[1])
    enabled = parents[page]
    choice = parents[enabled]
    assert enabled.get("test") == ">0"
    selection = parameters[refs[choice.get("ParamRefId")]]
    assert selection.get("Name") == f"IOHC_c{channel}ChannelSelection"
    assert page.find("k:ParameterBlock[@Name='IOHC_ProductFunctions']", NS) is None
    products = page.find("k:ParameterBlock[@Name='IOHC_Functions']/k:ParameterBlock[@Name='IOHC_ProductFunctions']", NS)
    expert = page.find("k:ParameterBlock[@Name='IOHC_ExpertOptions']", NS)
    diagnostics = page.find("k:ParameterBlock[@Name='IOHC_Diagnostics']", NS)
    assert products is not None and expert is not None and diagnostics is not None
    assert expert.find(".//k:ParameterBlock[@Name='IOHC_Diagnostics']", NS) is None
    for category in ('Overview', 'Sensors', 'Objects', 'Products'):
        assert diagnostics.find(f".//k:ParameterBlock[@Name='IOHC_Diagnostic{category}']", NS) is not None
    product_refs = products.findall(".//k:ParameterRefRef", NS)
    assert len(product_refs) == 4
    for ref in product_refs:
        param = parameters[refs[ref.get("RefId")]]
        assert re.match(rf"(?:PIC|PVX)_c{channel}(?!\d)", param.get("Name"))
    assert len(products.findall(".//k:ComObjectRefRef", NS)) == 12
    for ref in products.findall(".//k:ComObjectRefRef", NS):
        obj = objects[object_refs[ref.get("RefId")]]
        assert re.match(rf"(?:PIC|PVX)_c{channel}(?!\d)", obj.get("Name"))
    commissioning = page.find("k:ParameterBlock[@Name='IOHC_Commissioning']", NS)
    for ref in commissioning.findall(".//k:ParameterRefRef", NS):
        name = parameters[refs[ref.get("RefId")]].get("Name")
        assert not any(word in name for word in ("Recognition", "Sensor", "Object", "Context", "PairingDiag", "Imported")), name
assert len(dynamic.findall(".//k:ParameterBlock[@Name='IOHC_ProductFunctions']", NS)) == 16
assert len(dynamic.findall(".//k:ParameterBlock[@Name='IOHC_ExpertOptions']", NS)) == 16
assert len(dynamic.findall(".//k:ParameterBlock[@Name='IOHC_Diagnostics']", NS)) == 16
# The speed object belongs to its own channel and appears only for 2W covers.
movement_pages = dynamic.findall(".//k:ParameterBlock[@Name='IOHC_MovementMode']", NS)
assert len(movement_pages) == 16
movement_type = tree.find(".//k:ParameterType[@Name='MVSMovementMode']", NS)
assert {n.get("Value") for n in movement_type.findall(".//k:Enumeration", NS)} == {"0", "1", "2"}
assert not any(parameters[refs[ref.get("RefId")]].get("Name").endswith("SilentOperation")
               for ref in dynamic.findall(".//k:ParameterRefRef", NS))
for channel, movement in enumerate(movement_pages, 1):
    for ref in movement.findall(".//k:ParameterRefRef", NS):
        assert parameters[refs[ref.get("RefId")]].get("Name").startswith(f"MVS_c{channel}MovementMode")
        assert ref.get("HelpContext") == "IOHC-Fahrmodus"
    ko_ref = movement.find(".//k:ComObjectRefRef", NS)
    obj = objects[object_refs[ko_ref.get("RefId")]]
    assert int(obj.get("Number")) == 1200 + channel - 1
    assert obj.get("DatapointType") == "DPST-5-10"
    assert parents[ko_ref].get("test") == "1"
    assert parents[movement].get("test") == "1 2"
    protocol_when = parents[parents[parents[movement]]]
    assert protocol_when.get("test") == "0"
    assert parameters[refs[parents[protocol_when].get("ParamRefId")]].get("Name").endswith("ProtocolMode")
help_topics = {n.get("HelpContext") for n in dynamic.iter() if n.get("HelpContext", "").startswith("IOHC-")}
for channel in tree.findall(".//k:Channel[@Name='IOHC_Global']", NS):
    for ref in channel.findall(".//k:ParameterRefRef", NS):
        assert ref.get("HelpContext"), ref.get("RefId")
help_source = ROOT / "lib/OFM-IOHomeControl/src/Baggages/Help_de"
for topic in help_topics:
    assert (help_source / f"{topic}.md").is_file(), topic
archives = list((ROOT / "src/IoHomecontrol.baggages").rglob("Help_de.zip"))
assert any(help_topics <= {Path(name).stem for name in zipfile.ZipFile(archive).namelist()}
           for archive in archives), "Generated help archive lacks channel help"
print(f"16 channel trees and {len(help_topics)} contextual help topics verified")
