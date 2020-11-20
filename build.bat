echo '[INFO] Building debug cam-server'
echo '[WARN] Do not use in a production enviroment'
pause
echo '[INFO] Installing dependencies'
pip install pyinstaller flask
echo '[INFO] Installed pyinstaller and flask'
echo '[INFO] Building to dist'
pyinstaller -F cam_run.py
