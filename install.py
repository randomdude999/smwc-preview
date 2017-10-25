#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess

# i'm not using f-strings here because i want the user to see the "outdated python" message

pjoin = os.path.join
script_dir = os.path.dirname(os.path.abspath(__file__))


def userscript_install():
    if os.name == 'nt':
        import winreg
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\Classes\\x-smwc-preview")
        winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, "")
        winreg.SetValue(key, "", winreg.REG_SZ, "SMWC Preview")
        subkey = winreg.CreateKey(key, "shell\\open\\command")
        winreg.SetValue(subkey, "", winreg.REG_SZ, '"%s" "%%1"' % os.path.abspath("uri_handler\\smwc_uri_handler.bat"))
        winreg.CloseKey(subkey)
        winreg.CloseKey(key)
    else:
        script_path = os.path.join(script_dir, "uri_handler", "smwc_uri_handler.py")
        os.chmod(script_path, 0o775)
        with open("uri_handler/desktop-entry.template.desktop") as f:
            out = f.read().replace("@SCRIPT_PATH@", script_path)
        with open(os.path.expanduser("~/.local/share/applications/smwc-preview.desktop"), 'w') as f:
            f.write(out)
        subprocess.run(["xdg-mime", "default", "smwc-preview.desktop", "x-scheme-handler/x-smwc-preview"])

    with open("install_mode", 'w') as f:
        f.write("userscript_install")

    print("Install userscript.js as a userscript in your browser.")


def normal_install():
    msg_host_name = "randomdude999.smwc_preview"
    if os.name == 'nt':
        script_path = "chrome_native_messaging_host.bat"
    else:
        script_path = pjoin(script_dir, "native_messaging_host", "chrome_native_messaging_host.py")

    with open(pjoin("native_messaging_host", "smwc_preview.template.json")) as template_f:
        template = template_f.read()
    with open(pjoin("native_messaging_host", "smwc_preview.json"), 'w') as target_f:
        target_f.write(template.replace("@SCRIPT_PATH@", script_path))

    if os.name == 'nt':
        import winreg
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\Google\\Chrome\\NativeMessagingHosts\\%s" % msg_host_name)
        winreg.SetValue(key, "", winreg.REG_SZ, os.path.join(script_dir, "native_messaging_host\\smwc_preview.json"))
        winreg.CloseKey(key)
    elif os.name == 'posix':
        os.chmod(script_path, 0o775)
        if sys.platform.startswith('darwin'):
            target_path = "~/Library/Application Support/Google/Chrome/NativeMessagingHosts/%s.json" % msg_host_name
        elif sys.platform.startswith('linux'):
            target_path = "~/.config/google-chrome/NativeMessagingHosts/%s.json" % msg_host_name
        else:
            print("What system are u on dude (not windows, not osx, not linux... my best guess would be *bsd)")
            return
        target_path = os.path.expanduser(target_path)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        shutil.copyfile("native_messaging_host/smwc_preview.json", target_path)

    with open("install_mode", 'w') as f:
        f.write("normal_install")

    print("Installed. Make sure to also install chrome_ext.crx if you haven't already.")


def main():
    if sys.version_info[0] < 3 or sys.version_info[0] == 3 and sys.version_info[1] < 6:
        print("Your python version is outdated. This application requires "
              "at least Python version 3.6, but you have",
              str(sys.version_info[0]) + "." + str(sys.version_info[1]) +
              ". (Also, make sure that running 'python3' executes 3.6+, "
              "or stuff will silently fail)")
        return

    if os.name != 'nt':
        if shutil.which("zenity") is None:
            print("You don't have zenity installed. zenity is the way I show "
                  "message boxes (on non-windows systems). Please also install"
                  " that before using this application.\n"
                  "For linux, it should be in the repos for your os.")
            if sys.platform == 'darwin':
                print("For osx, it's available through homebrew.\n"
                      "I hope i'll figure out OSX native dialogs soon but i "
                      "don't have a mac so that could be complicated")

    if os.name == 'nt' or sys.platform.startswith("linux"):
        inp = input("Install in userscript mode? (this is recommended if you "
                    "don't want to install a developer-mode extension) [Y/n] ")
        if not inp.lower().startswith("n"):
            userscript_install()
            return

    normal_install()
    if not os.path.exists(os.path.join(script_dir, "settings.json")):
        print("It appears settings.json is missing. "
              "Please also run gen_settings.py.")

if __name__ == '__main__':
    main()
