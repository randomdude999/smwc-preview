import subprocess
import zipfile
import fnmatch
import os

# needed for building the extension
chrome_exe = os.environ["CHROME_EXE"]


exclude_from_zip = [
    ".idea",
    "settings.json",
    "gen_zip.py",
    ".gitignore",
    "chrome_ext.pem",
    "install_mode",
    "smwc_preview.zip",
    os.path.join("*", "error.log"),
    os.path.join("native_messaging_host", "smwc_preview.json"),
    ".git",
    os.path.join("*", "__pycache__"),
    "*.py[co]",
    "README_user.txt",
    "README.md",
    os.path.join("uri_handler", "uri_format.txt")
]

if os.path.exists("chrome_ext.pem"):
    result = subprocess.run([chrome_exe,
                             "--pack-extension=" + os.path.abspath("chrome_ext"),
                             "--pack-extension-key=" + os.path.abspath("chrome_ext.pem")])
    if result.returncode != 0:
        print(f"chrome exited with error code {result.returncode}")

with zipfile.ZipFile('smwc_preview.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk("."):
        for x in dirs.copy():  # iterate over copy but modify original, modifying the thing you're iterating is bad and causes cryptic errors
            root_relative_path = os.path.join(root if root != '.' else '', x)
            for pattern in exclude_from_zip:
                if fnmatch.fnmatch(root_relative_path, pattern):
                    dirs.remove(x)
                    break
        for x in files:
            root_relative_path = os.path.join(root if root != '.' else '', x)
            include = True
            for pattern in exclude_from_zip:
                if fnmatch.fnmatch(root_relative_path, pattern):
                    include = False
                    break
            if include:
                zipf.write(root_relative_path)
    zipf.write("README_user.txt", "README.txt")
