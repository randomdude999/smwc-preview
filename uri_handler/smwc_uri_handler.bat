@echo off
cd %~dp0
start pyw -3 %~dp0smwc_uri_handler.py %* >%~dp0error.log 2>&1