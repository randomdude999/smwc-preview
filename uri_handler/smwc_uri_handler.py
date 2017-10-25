#!/usr/bin/env python3
import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "python_code"))
)

os.chdir(os.path.join(os.path.dirname(__file__), ".."))

# Redirect stdout/stderr to a file for better debugging
fsock = open(os.path.join(os.path.dirname(__file__), 'error.log'), 'w')
sys.stdout = sys.stderr = fsock

print(os.getcwd())

import smwc_preview_start


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
