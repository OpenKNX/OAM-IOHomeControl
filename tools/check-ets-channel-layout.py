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
    products = page.find("k:ParameterBlock[@Name='IOHC_Functions']", NS)
    assert products.findall(".//k:ParameterBlock", NS) == []
    expert = page.find("k:ParameterBlock[@Name='IOHC_ExpertOptions']", NS)
    diagnostics = page.find("k:ParameterBlock[@Name='IOHC_Diagnostics']", NS)
    assert products is not None and expert is not None and diagnostics is not None
    assert expert.find(".//k:ParameterBlock[@Name='IOHC_Diagnostics']", NS) is None
    profile_tab = expert.find(".//k:ParameterBlock[@Name='IOHC_ExpertControllerProfile']", NS)
    profile_condition = parents[profile_tab]
    assert profile_condition.get("test") == "1"
    assert parameters[refs[parents[profile_condition].get("ParamRefId")]].get("Name") == f"IOHC_c{channel}ProtocolMode"
    for category in ('Overview', 'Sensors', 'Objects', 'Products'):
        assert diagnostics.find(f".//k:ParameterBlock[@Name='IOHC_Diagnostic{category}']", NS) is not None
    product_refs = [ref for ref in products.findall(".//k:ParameterRefRef", NS)
                    if parameters[refs[ref.get("RefId")]].get("Name").startswith(("PIC_", "PVX_"))]
    assert len(product_refs) == 4
    for ref in product_refs:
        ancestor = ref
        while ancestor is not products:
            parent = parents[ancestor]
            if parent.tag.endswith('choose') and parent.get('ParamRefId') in refs:
                parameter = parameters[refs[parent.get('ParamRefId')]]
                if parameter.get('Name') == f'IOHC_c{channel}DeviceType':
                    allowed = {int(v) for v in ancestor.get('test').split()}
                    name = parameters[refs[ref.get('RefId')]].get('Name')
                    assert allowed == ({25,26} if name.startswith('PIC_') else {18,21,22,23,30})
                    break
            ancestor = parent
        else:
            raise AssertionError('Product settings are missing their device-type condition')
    for ref in product_refs:
        param = parameters[refs[ref.get("RefId")]]
        assert re.match(rf"(?:PIC|PVX)_c{channel}(?!\d)", param.get("Name"))
    product_kos = [ref for ref in products.findall(".//k:ComObjectRefRef", NS)
                   if objects[object_refs[ref.get("RefId")]].get("Name").startswith(("PIC_", "PVX_"))]
    assert len(product_kos) == 12
    for ref in product_kos:
        obj = objects[object_refs[ref.get("RefId")]]
        assert re.match(rf"(?:PIC|PVX)_c{channel}(?!\d)", obj.get("Name"))
    commissioning = page.find("k:ParameterBlock[@Name='IOHC_Commissioning']", NS)
    for ref in commissioning.findall(".//k:ParameterRefRef", NS):
        name = parameters[refs[ref.get("RefId")]].get("Name")
        assert not any(word in name for word in ("Recognition", "Sensor", "Object", "Context", "PairingDiag", "Imported")), name
assert not dynamic.findall(".//k:ParameterBlock[@Name='IOHC_ProductFunctions']", NS)
assert len(dynamic.findall(".//k:ParameterBlock[@Name='IOHC_ExpertOptions']", NS)) == 16
assert len(dynamic.findall(".//k:ParameterBlock[@Name='IOHC_Diagnostics']", NS)) == 16
# The speed object belongs to its own channel and appears only for 2W covers.
movement_pages = [ref for ref in dynamic.findall(".//k:ParameterRefRef", NS)
                  if re.fullmatch(r"MVS_c\d+MovementMode", parameters[refs[ref.get("RefId")]].get("Name"))]
assert len(movement_pages) == 16
movement_type = tree.find(".//k:ParameterType[@Name='MVSMovementMode']", NS)
assert {n.get("Value") for n in movement_type.findall(".//k:Enumeration", NS)} == {"0", "1", "2"}
assert not any(parameters[refs[ref.get("RefId")]].get("Name").endswith("SilentOperation")
               for ref in dynamic.findall(".//k:ParameterRefRef", NS))
for channel, movement in enumerate(movement_pages, 1):
    assert parameters[refs[movement.get("RefId")]].get("Name") == f"MVS_c{channel}MovementMode"
    assert movement.get("HelpContext") == "IOHC-Fahrmodus"
    expected_choices = {1}
    assert {int(v) for v in parents[movement].get("test").split()} == expected_choices
    protocol_when = parents[parents[parents[movement]]]
    assert protocol_when.get("test") == "0"
    assert parameters[refs[parents[protocol_when].get("ParamRefId")]].get("Name").endswith("ProtocolMode")
    functions = parents[parents[protocol_when]]
    assert functions.get("Name") == "IOHC_Functions"
    ko_refs = [ref for ref in functions.findall(".//k:ComObjectRefRef", NS)
               if objects[object_refs[ref.get("RefId")]].get("Name") == f"MVS_c{channel}MovementMode"]
    assert len(ko_refs) == 1
    ko_ref = ko_refs[0]
    obj = objects[object_refs[ko_ref.get("RefId")]]
    assert int(obj.get("Number")) == 1200 + channel - 1
    assert obj.get("DatapointType") == "DPST-5-10"
    assert parents[ko_ref].get("test") == "1"
# Every exact profile exposes only its named and supported MP/FP functions.
registry=(ROOT / "lib/OFM-IOHomeControl/src/protocol/IoHomeProfileRegistry.cpp").read_text().split("constexpr IoHomeParameterAlias")[0]
profile_maps={}
for code, args in re.findall(r'profile\((0x[0-9A-F]+), "[^\"]+", (.*?)\)',registry,re.S):
    semantics=(re.findall(r'S::(\w+)',args)+['Unsupported']*4)[:4]
    values={i:name for i,name in enumerate(semantics) if name!='Unsupported'}
    packed=int(code,16)
    if packed==0x0082:values[9]='ProjectionAngle'
    if packed==0x0241:values[1]='WindowSecurityMode'
    profile_maps[packed]=values
for page in pages:
    channel=int(re.search(r"Channel(\d+)Page",page.get("Name"))[1])
    functions=page.find("k:ParameterBlock[@Name='IOHC_Functions']",NS)
    selectors=[choose for choose in functions.findall('.//k:choose',NS)
               if parameters[refs[choose.get('ParamRefId')]].get('Name')==f'PRF_c{channel}ProfileCode'
               and choose.find("k:when[@test='0']",NS) is not None]
    assert len(selectors)==1
    selector=selectors[0]
    assert parents[selector].get('test')=='1'
    assert parameters[refs[parents[parents[selector]].get('ParamRefId')]].get('Name')==f'PRF_c{channel}Enabled'
    assert {int(w.get('test')) for w in selector.findall('k:when',NS)} == {0,*profile_maps}
    for packed, values in profile_maps.items():
        branch=selector.find(f"k:when[@test='{packed}']",NS)
        numbers=[]
        for ref in branch.findall('k:ComObjectRefRef',NS):
            obj=objects[object_refs[ref.get('RefId')]]
            numbers.append(int(obj.get('Number'))-(1300+18*(channel-1)))
        expected=[]
        for index,semantic in values.items():
            slot=(0,1,2,3,9).index(index)
            binary=index==0 and (packed&63==58 or semantic in ('LockState','SwitchState'))
            if semantic not in ('ProjectionAngle','WindowSecurityMode'):expected.append(16 if binary else slot*3)
            expected.extend([17 if binary else slot*3+1,slot*3+2])
        assert numbers==expected,(channel,packed,numbers,expected)
        if packed==0x0241:
            security=branch.findall('k:ComObjectRefRef',NS)[-2]
            ref_id=security.get('RefId')
            object_ref=tree.find(f".//k:Static//k:ComObjectRef[@Id='{ref_id}']",NS)
            assert object_ref.get('DatapointType')=='DPST-5-10'
    assert not functions.findall('.//k:ParameterBlock',NS)
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
