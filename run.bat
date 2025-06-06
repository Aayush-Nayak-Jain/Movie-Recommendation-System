@echo off
if exist manage.py (
    echo Starting Django development server...
    start "" "http://127.0.0.1:8000"
    cmd /c python manage.py runserver --noreload
    pause
) else (
    echo Error: manage.py not found in current directory!
    pause
)