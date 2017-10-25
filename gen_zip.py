import subprocess
import zipfile
import os

# this is a little hacky
# okay, very hacky and also error-prone
# i'll replace this soon

chrome_exe = os.environ["CHROME_EXE"]

to_zip = [
    "native_messaging_host\\chrome_native_messaging_host.bat",
    "native_messaging_host\\chrome_native_messaging_host.py",
    "native_messaging_host\\common.py",
    "native_messaging_host\\smwc_hack_play.py",
    "native_messaging_host\\smwc_music_preview.py",
    "native_messaging_host\\smwc_preview.template.json",
    "native_messaging_host\\smwc_sram_play.py",
    "chrome_ext\\background.js",
    "chrome_ext\\content.js",
    "chrome_ext\\manifest.json",
    "uri_handler\\smwc_uri_handler.bat",
    "uri_handler\\smwc_uri_handler.py",
    "uri_handler\\uri_format.txt",
    "python_code\\"
    "gen_settings.py",
    "install.py",
    "README.txt",
    "uninstall.py"
]

result = subprocess.run([chrome_exe,
                         "--pack-extension=" + os.path.abspath("chrome_ext"),
                         "--pack-extension-key=" + os.path.abspath("chrome_ext.pem")])
if result.returncode != 0:
    print(f"chrome exited with error code {result.returncode}")

with zipfile.ZipFile('smwc_preview.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    for x in to_zip:
        zipf.write(x)
    zipf.write("chrome_ext.crx")
