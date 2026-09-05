pyinstaller --noconsole --onedir --contents-directory "." lichvannien.py
if exist dist\lichvannien (
    xcopy /y "flip_calendar.wav" "dist\lichvannien\"
)
