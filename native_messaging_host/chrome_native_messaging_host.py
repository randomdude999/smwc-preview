#!/usr/bin/env python3
import json
import struct
import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "python_code"))
)

os.chdir(os.path.join(os.path.dirname(__file__), ".."))

# Redirect stdout/stderr to a file for better debugging
fsock = open(os.path.join(os.path.dirname(__file__), 'error.log'), 'w')
sys.stdout = sys.stderr = fsock

import smwc_preview_start

# Most of this is taken from google's native messaging example code.
while True:
    # Read the message length (first 4 bytes).
    text_length_bytes = sys.stdin.buffer.read(4)
    if len(text_length_bytes) == 0:
        sys.exit(0)
    # Unpack message length as 4 byte integer.
    text_length = struct.unpack('i', text_length_bytes)[0]
    # Read the text (JSON object) of the message.
    text = sys.stdin.buffer.read(text_length).decode('utf-8')
    data = json.loads(text)
    smwc_preview_start.do_stuff(data)
