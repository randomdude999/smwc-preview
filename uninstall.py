import sys
import os

try:
    with open("install_mode") as f:
        install_mode = f.read()
except FileNotFoundError:
    install_mode = "normal_install"


if install_mode == "userscript_install":
    if sys.platform == 'win32':
        import winreg
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, "Software\\Classes\\x-smwc-preview")
elif install_mode == "normal_install":
    msg_host_name = "randomdude999.smwc_preview"
    if sys.platform == 'win32':
        import winreg
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, f"Software\\Google\\Chrome\\NativeMessagingHosts\\{msg_host_name}")
    elif sys.platform.startswith('darwin'):
        os.remove(os.path.expanduser(f"~/Library/Application Support/Google/Chrome/NativeMessagingHosts/{msg_host_name}.json"))
    elif sys.platform.startswith('linux'):
        os.remove(os.path.expanduser(f"~/.config/google-chrome/NativeMessagingHosts/{msg_host_name}.json"))

print("Uninstalled. You can delete this directory now.")
if install_mode == "normal_install":
    print("Don't forget to remove the chrome extension.")
