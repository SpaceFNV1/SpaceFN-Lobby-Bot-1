@echo off
ECHO Installing the required packages for the bot!
TIMEOUT 3

py -3 -m pip install -U -r commands.txt

ECHO Done! Now run LOBBY BOT.bat
PAUSE