@echo off
py -3 %~dp0chrome_native_messaging_host.py %* >%~dp0error.log 2>&1