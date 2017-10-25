import hashlib
import shlex
import json
import os

# Must have for interactive scripts
try:
    import readline
except ImportError:
    try:
        # noinspection PyUnresolvedReferences
        import pyreadline as readline
    except ImportError:
        pass

script_dir = os.path.dirname(os.path.abspath(__file__))


def get_prog(name, check=None, is_dir=False):
    type_check = os.path.isdir if is_dir else os.path.isfile
    while True:
        prog_path = input(f"Drag and drop {name}: ")
        if os.name == 'nt':
            # on windows, drag-n-dropping paths with spaces in them adds quotes
            prog_path = prog_path.strip('"')
        else:
            # on posix, we can parse the drag-n-dropped path as a command argument (on my terminal, anyways)
            if len(shlex.split(prog_path)) == 1:
                prog_path = shlex.split(prog_path)[0]
        if len(prog_path) == 0:
            break
        if type_check(prog_path) and os.path.isabs(prog_path):
            if check:
                check(prog_path)
            break
        print("Invalid path.")
    return prog_path


def check_smw(path):
    with open(path, 'rb') as f:
        if path.endswith('.smc'):
            f.seek(512)
        if hashlib.sha1(f.read()).hexdigest() != "6b47bb75d16514b6a476aa0c73a683a2a4c18765":
            print("Warning: This doesn't appear to be a clean USA SMW rom.")


def check_yi(path):
    with open(path, 'rb') as f:
        if path.endswith('.smc'):
            f.seek(512)
        digest = hashlib.sha1(f.read()).hexdigest()
        if digest != "c807f2856f44fb84326fac5b462340dcdd0471f8":
            print("Warning: This doesn't appear to be a clean USA YI 1.0 rom.")
        if digest == "34612a93741f156d6e497462ab7f253cb8a959a0":
            print("This is a version 1.1 rom, but hacks require the 1.0 rom.")


with open(os.path.join(script_dir, "settings.json"), 'w') as settings:
    settings.write(json.dumps({
        'flips_loc': get_prog("flips.exe"),
        'emu_loc': get_prog("your favorite emulator"),
        'emu_saves_loc': get_prog("emulator's saves directory (not states!)", is_dir=True),
        'smw_loc': get_prog("a clean SMW rom", check_smw),
        'yi_loc': get_prog("a clean YI rom", check_yi),
        'spcplay_loc': get_prog("spcplay.exe"),
    }))
