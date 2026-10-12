@echo off
cd /d "%~dp0.."
python main.py --vfs examples\minimal.xml --debug-config
