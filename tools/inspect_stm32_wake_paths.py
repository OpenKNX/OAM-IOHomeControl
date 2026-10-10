#!/usr/bin/env python3
"""Reproduce bounded Thumb call-site evidence; does not infer indirect PRIVATE producers.
Requires capstone (install into a venv or a temporary --target directory).
"""
import argparse, hashlib, json, struct
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB, CS_MODE_LITTLE_ENDIAN
BASE=0x08000000
REGIONS={'prefix_selector':(0x080139B8,0x080139E2),
         'low_power_setter':(0x0800E6DC,0x0800E6EC),
         'ctrl1_bit5_setter':(0x08013C78,0x08013C86),
         'shared_2w_prepare':(0x0800FE5C,0x0800FFA8),
         'session_submit_wrapper':(0x0800FFB0,0x0800FFE6),
         'longer_session_state':(0x08010970,0x0801099E)}
TARGETS={0x080139B8:'prefix_selector',0x0800FE5C:'shared_2w_prepare',0x0800FFB0:'session_submit_wrapper'}
def inspect(path):
    data=Path(path).read_bytes()
    expected='e0c20192affea4bc02514fd19d460b85a95f429b5834e53f1970a0018f946529'
    if len(data)!=262144 or hashlib.sha256(data).hexdigest()!=expected:
        raise ValueError('This address map is qualified only for the supplied 2022 STM32 image')
    md=Cs(CS_ARCH_ARM,CS_MODE_THUMB|CS_MODE_LITTLE_ENDIAN)
    def instructions(start,end):
        return [dict(address=f'0x{i.address:08X}',mnemonic=i.mnemonic,operands=i.op_str)
                for i in md.disasm(data[start-BASE:end-BASE],start)]
    direct=[]
    for offset in range(0,len(data)-4,2):
        insn=next(md.disasm(data[offset:offset+4],BASE+offset,count=1),None)
        if insn and insn.mnemonic in ('bl','b.w') and insn.op_str.startswith('#0x'):
            target=int(insn.op_str[1:],16)
            if target in TARGETS:
                direct.append(dict(address=f'0x{insn.address:08X}',target=TARGETS[target],
                                   preceding=instructions(insn.address-12,insn.address+4)))
    # Prefix selector is commonly virtual. Literal pointers are evidence of a
    # reference, not proof that a given request reached this target.
    pointers=[f'0x{BASE+offset:08X}' for offset in range(0,len(data)-4,2)
              if struct.unpack_from('<I',data,offset)[0]==0x080139B9]
    return dict(sha256=hashlib.sha256(data).hexdigest(),size=len(data),
        regions={name:instructions(*bounds) for name,bounds in REGIONS.items()},
        direct_branch_candidates=direct,thumb_pointer_references=pointers,
        conclusion='Shared preparation clears CTRL1 bit 5; real PRIVATE 0x03 selection of 1960 is unproven.',
        limitations=['Halfword scanning may include embedded data; inspect each call in context.',
                     'Indirect calls and concrete PRIVATE START producers are not exhaustively resolved.',
                     'Gateway code cannot establish actuator RX duty-cycle intervals.',
                     'No hardware RF waveform or channel-wake pattern was measured.'])
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('dump');args=parser.parse_args()
    print(json.dumps(inspect(args.dump),indent=2))
