@echo off
cd /d "%~dp0.."
python main.py --vfs examples\demo.xml --script examples\quotes.txt --debug-config
