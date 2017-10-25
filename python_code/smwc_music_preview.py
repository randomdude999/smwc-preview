import os
import subprocess
from tempfile import mkstemp

import common


def play_raw_data(data, _):
    (fd, fpath) = mkstemp(".spc")
    os.write(fd, data)
    os.close(fd)
    subprocess.run([common.settings['spcplay_loc'], fpath], stdout=subprocess.DEVNULL)
    os.remove(fpath)


def play_id(item_id):
    if not common.check("music", (("spcplay_loc", "SPC player"),)):
        return
    (success, zip_data) = common.download(item_id)
    if not success:
        return
    common.choose_with_dialogs(zip_data, "spc", play_raw_data, "SPCs")
