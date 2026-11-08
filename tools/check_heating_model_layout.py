#!/usr/bin/env python3
"""Compare generated ETS macros to the application baseline; preserve all old offsets."""
import argparse
import json
import re
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--baseline', default='f275a26d65449a8f728fc51a536312f74a76360d')
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
old = subprocess.check_output(['git', 'show', args.baseline + ':include/knxprod.h'], cwd=root, text=True)
new = (root / 'include/knxprod.h').read_text()
parse = lambda s: dict(re.findall(r'^#define\s+(\w+)(.*)$', s, re.M))
a, b = parse(old), parse(new)
changes = {k: [v, b.get(k)] for k, v in a.items() if b.get(k) != v}
added = {k: v for k, v in b.items() if k not in a}
assert changes == {'MAIN_ApplicationVersion': [' 73', ' 74'], 'IOHC_ModuleVersion': [' 9', ' 10']}, changes
assert set(added) == {'HTG_cModel', 'HTG_cModelMask', 'HTG_cModelShift', 'ParamHTG_cModel'}, added
assert b['HTG_ParamBlockSize'].strip() == '3'
assert b['HTG_cModelMask'].strip() == '0x18'
assert b['HTG_cModelShift'].strip() == '3'
print(json.dumps({'baseline': args.baseline, 'existingMacros': len(a), 'changes': changes, 'added': added, 'allOtherExistingMacrosUnchanged': True}, indent=2))
