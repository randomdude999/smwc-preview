#!/usr/bin/env python3
import sys
import os
sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "python_code")
)

# noinspection PyPep8
import smwc_preview_start

# 95% of this is validation.
# You can't even really do any harm if i hadn't done all the validation, but whatevs


def error(msg):
    print(msg)
    sys.exit(1)

if len(sys.argv) != 2:
    error("Ivalid number of arguments to script")

if not sys.argv[1].startswith("x-smwc-preview:"):
    error("invalid protocol")
params = sys.argv[1].replace("x-smwc-preview:", "").split(',')
if len(params) not in (2, 3):
    error("Invalid number of comma-separated parameters")

# noinspection PyDictCreation
result = {}

result['type'] = params[0]
if result['type'] not in smwc_preview_start.ALL_TYPES:
    error("invalid preview type")
result['id'] = params[1]
if not result['id'].isnumeric():
    error("id not numeric")
if result['type'] in smwc_preview_start.NEEDS_SECONDARY_ID:
    if len(params) != 3:
        error("invalid number of parameters")
    result['secondary_id'] = params[2]
    if not result['secondary_id'].isnumeric():
        error("secondary id not numeric")
else:
    if len(params) != 2:
        error("invalid number of parameters")

smwc_preview_start.do_stuff(result)
