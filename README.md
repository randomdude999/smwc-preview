# SMWC Preview

Adds preview support to SMWC.

Also read README_user.txt, that is the readme included in the generated ZIP.

## How it works

There are two main modes of installation: normal install and userscript
install. Normal installation installs a Chrome extension that sends a native
message when the user clicks "Preview" and a native messaging host that then
previews the content. Userscript installation works by regsitering a protocol
handler to show previews and a userscript to add a "Preview" link that links to
the protocol. The URI format is documented in `uri_handler/uri_format.txt` and
is very strictly verified.

## Platform support

|                | Normal  | Userscript |
|----------------|---------|------------|
| Chrome         | Yes     | Yes        |
| Other browsers | No      | Yes        |
| Windows        | Yes [1] | Yes        |
| Mac OS X       | Maybe   | No         |
| Linux          | Yes     | Yes        |

[1] The extension needs to be loaded as an unpacked extension, which shows an
annoying pop-up every time you start chrome.

## Project Structure

* `chrome_ext` contains the source code of the Chrome extension when installing
in normal mode.
* `native_messaging_host` contains files related to the native messaging part
of the normal mode install.
* `python_code` contains code shared by both the userscript install and normal
install.
* `uri_handler` contains files related to the URI handler when using the
userscript install.