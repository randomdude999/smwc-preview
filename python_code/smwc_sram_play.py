import os
import subprocess
from io import BytesIO
from tempfile import mkstemp
from zipfile import ZipFile

import common
import smwc_hack_play


def choose_with_dialogs_and_return(zip_data, ftype, type_plural):
    with ZipFile(BytesIO(zip_data)) as myzip:
        files = []
        for x in myzip.namelist():
            if x.endswith("." + ftype):
                files.append(x)
        if len(files) == 0:
            common.message(f"No {type_plural} found in zip!", True)
        elif len(files) == 1:
            return myzip.read(files[0])
        else:
            common.message(f"Multiple {type_plural} found in zip.\n" + '\n'.join(files))
            for x in files:
                result = common.message(f"Play {x}?", multi_buttons=True)
                if result == "yes":
                    return myzip.read(x)
                if result == "no":
                    continue
                if result == "cancel":
                    break


def play_id(sram_id, hack_id):
    # checks: flips, emulator, smw rom, emu saves dir
    common.check("hack", (("flips_loc", "Flips"),
                          ("emu_loc", "emulator"),
                          ("smw_loc", "Super Mario World ROM"),
                          ("emu_saves_loc", "emulator saves directory")))
    (success, sram_zip) = common.download(sram_id)
    if not success:
        return
    (success, hack_zip) = common.download(hack_id)
    if not success:
        return
    with ZipFile(BytesIO(sram_zip)) as myzip:
        files = []
        for x in myzip.namelist():
            if x.endswith(".srm"):
                files.append(x)
        if len(files) > 1:
            common.message("Found multiple SRM files in the zip and don't know what to do", True)
            return
        sram_data = myzip.read(files[0])
    hack_data = choose_with_dialogs_and_return(hack_zip, "bps", "patches")
    if not hack_data:
        return
    (fd, bps_path) = mkstemp(".bps")
    os.write(fd, hack_data)
    os.close(fd)
    rom_path = smwc_hack_play.apply_flips(False, bps_path)
    os.remove(bps_path)
    if not rom_path:
        return
    sram_loc = os.path.join(common.settings['emu_saves_loc'], os.path.basename(rom_path).replace(".smc", ".srm"))
    with open(sram_loc, 'wb') as f:
        f.write(sram_data)
    subprocess.run([common.settings['emu_loc'], rom_path], stdout=subprocess.DEVNULL)
    os.remove(sram_loc)
    os.remove(rom_path)
