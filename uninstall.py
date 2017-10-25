import sys
import os

msg_host_name = "randomdude999.smwc_preview"
if sys.platform == 'win32':
    import winreg
    winreg.DeleteKey(winreg.HKEY_CURRENT_USER, f"Software\\Google\\Chrome\\NativeMessagingHosts\\{msg_host_name}")
elif sys.platform.startswith('darwin'):
    os.remove(os.path.expanduser(f"~/Library/Application Support/Google/Chrome/NativeMessagingHosts/{msg_host_name}.json"))
elif sys.platform.startswith('linux'):
    os.remove(os.path.expanduser(f"~/.config/google-chrome/NativeMessagingHosts/{msg_host_name}.json"))

print("Uninstalled. You can delete this directory now. Don't forget to remove the chrome extension.")