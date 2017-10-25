import os
import shutil
import subprocess
from functools import partial
from tempfile import mkdtemp

from python_code import common


def apply_flips(is_yi, bps_path):
    base_rom = common.settings['yi_loc'] if is_yi else common.settings['smw_loc']
    rom_path = bps_path.replace('.bps', '.smc')
    result = subprocess.run([common.settings['flips_loc'], '-a', bps_path, base_rom, rom_path], stdout=subprocess.PIPE)
    if result.returncode != 0:
        common.message("Error applying patch. Flips output:\n" + result.stdout.decode(), True)
        return
    return rom_path


def play_hack(is_yi, bps_data, bps_name):
    tempdir = mkdtemp()
    bps_name = bps_name.replace('/', '_')
    bps_path = os.path.join(tempdir, bps_name)
    with open(bps_path, 'wb') as f:
        f.write(bps_data)
    rom_path = apply_flips(is_yi, bps_path)
    if rom_path:
        subprocess.run([common.settings['emu_loc'], rom_path], stdout=subprocess.DEVNULL)
    shutil.rmtree(tempdir)


def play_id(item_id, is_yi):
    if not common.check("hack", (("flips_loc", "Flips"),
                                 ("emu_loc", "emulator"),
                                 ("yi_loc", "Yoshi's Island ROM") if is_yi else
                        ("smw_loc", "Super Mario World ROM"))):
        return

    (success, zip_data) = common.download(item_id)
    if not success:
        return

    common.choose_with_dialogs(zip_data, "bps", partial(play_hack, is_yi), "patches")
