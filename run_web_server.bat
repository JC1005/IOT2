cd /d %~dp0

cmd.exe /K "conda activate iot2 & python.exe web_server.py 80"

rem http://localhost