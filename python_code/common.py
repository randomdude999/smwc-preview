from zipfile import ZipFile
from io import BytesIO
import urllib.request
import subprocess
import ctypes
import json
import sys
import os


def message(msg, error_icon=False, multi_buttons=False):
    if os.name == 'nt':
        # The styles are a bit confusing, for an explanation, see
        # https://msdn.microsoft.com/en-us/library/windows/desktop/ms645505.aspx
        style = (0x10 if error_icon else 0x0) + (0x3 if multi_buttons else 0x0)
        result = ctypes.windll.user32.MessageBoxW(0, msg, "SMWC Preview", style)
        if multi_buttons:
            if result == 2:
                return "cancel"
            elif result == 6:
                return "yes"
            elif result == 7:
                return "no"
    else:
        # use zenity instead
        cmd = 'zenity --title="SMWC Preview"'
        if not multi_buttons:
            cmd += ' --error' if error_icon else ' --info'
        else:
            cmd += ' --question'
        cmd += f' --text="{msg}"'
        # zenity has no cancel button... :(
        if subprocess.run(cmd, shell=True).returncode == 1:
            return "no"
        else:
            return "yes"


try:
    with open("settings.json") as settings_file:
        settings = json.load(settings_file)
except (json.decoder.JSONDecodeError, FileNotFoundError):
    message("Your settings file is broken - try re-running gen_settings.py", True)
    sys.exit()


def check(kind, needs):
    for setting, name in needs:
        if not settings[setting] or not os.path.exists(settings[setting]):
            message(f"Can't play {kind} because {name} is missing\n(Try running gen_settings.py?)", True)
            return False
    return True


def download(item_id):
    with urllib.request.urlopen(f"https://dl.smwcentral.net/{item_id}/") as req:
        if req.getcode() == 200:
            return True, req.read()
        else:
            message(f"Download error: server responded with {req.getcode()}", True)
            return False, b''


def choose_with_dialogs(zip_data, ftype, func_to_apply, type_plural):
    with ZipFile(BytesIO(zip_data)) as myzip:
        files = []
        for x in myzip.namelist():
            if x.endswith("." + ftype):
                files.append(x)
        if len(files) == 0:
            message(f"No {type_plural} found in zip!", True)
        elif len(files) == 1:
            func_to_apply(myzip.read(files[0]), files[0])
        else:
            message(f"Multiple {type_plural} found in zip.\n"+'\n'.join(files))
            for x in files:
                result = message(f"Play {x}?", multi_buttons=True)
                if result == "yes":
                    func_to_apply(myzip.read(x), x)
                if result == "no":
                    continue
                if result == "cancel":
                    break
