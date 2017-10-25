SMWC PREVIEW 1.0
by randomdude999

This is a Chrome extension that adds a "Preview" / "Play" button to SMW Central
submissions.

INSTALL INSTRUCTIONS:
 - get yourself a Python 3.6 (https://www.python.org/) (if on windows, make
   sure to install the py launcher too)
 - If you are on Mac or Linux, get zenity (from your distro's repos or
   homebrew)
 - Run install.py
 - Run gen_settings.py
 - If you used "userscript install", install userscript.js in your browser.
   You're done.
 - Otherwise open chrome://extensions, then drag and drop chrome_ext.crx onto
   the Chrome window.
 - If you get errors about untrusted extensions or something, check the
   "Developer mode" checkbox and choose load unpacked extension, then browse
   to the chrome_ext folder. You can uncheck developer mode later.

UNINSTALLING:
 - Run uninstall.py
 - Remove the Chrome extension (or userscript)
 - Delete this folder

CHANGING INSTALL LOCATION:
 - Move the entire folder
 - Re-run install.py

ABOUT GEN_SETTINGS.PY:
 - spcplay.exe is needed for previewing music
 - flips.exe and emulator are needed for playing hacks (both SMW and YI)
 - ROMs are needed for playing their respective hacks
 - emulator's saves directory is needed for playing SRAM (.srm) files
   (from the Savebase)
 - Re-run gen_settings.py any time you move any of the tools it asked for.
 - It also automatically checks if your ROM is clean and the correct version.
 - If you don't want some feature, just leave it blank. The "Preview"/"Play"
   button will still be there, it just won't work.

STUFF YOU CAN PREVIEW:
 - SMW Music
 - BRR Samples
 - SMW Hacks
 - YI Hacks
 - SRAM files (from the SRAM database aka savebase)

ABOUT PREVIEWING:
 - This works by downloading the zip and scanning it for relevant files. Thus,
   zips inside zips are not recognized. Also, it adds one to the download
   counter each time you preview something.
 - If a zip contains multiple valid files, you'll be given a list of them and
   then asked if you want to play each one.
 - SRAM files are assumed to be for SMW hacks. If someone shows me one non-smw
   sram in the savebase, I'll fix this.
 - For music, you don't have to use spc700 player, but some others may not
   work.
 - You can only preview BRR zips that include demo SPCs. I might add support
   for BRR Player sometime in the future.
 - For playing hacks, savestates/SRAM will persist unless the emulator stores
   them right next to the ROM. (this is the default in most emulators, it can
   be changed by looking for something like directories or folder options in
   the emulator settings)
 - SRAM previews are sometimes broken because the link on the SRAM file's page
   links to an older version.