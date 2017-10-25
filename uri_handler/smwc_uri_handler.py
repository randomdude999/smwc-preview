import sys

import smwc_preview_start

# 90% of this is validation.
# You can't even really do any harm if i hadn't done all the validation, but whatevs

if len(sys.argv) != 2:
    sys.exit(1)

params = sys.argv[1].split(',')
if len(params) not in (2, 3):
    sys.exit(1)

# noinspection PyDictCreation
result = {}

result['type'] = params[0]
if result['type'] not in smwc_preview_start.ALL_TYPES:
    sys.exit(1)
result['id'] = params[1]
if not result['id'].isnumeric():
    sys.exit(1)
if result['type'] in smwc_preview_start.NEEDS_SECONDARY_ID:
    if len(params) != 3:
        sys.exit(1)
    result['secondary_id'] = params[2]
    if not result['secondary_id'].isnumeric():
        sys.exit(1)
else:
    if len(params) != 2:
        sys.exit(1)

smwc_preview_start.do_stuff(result)
