cd /d %~dp0

cmd.exe /K "conda activate IoT_assign & python.exe socket_server.py 127.0.0.1 8889"

