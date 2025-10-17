@echo off
echo Starting LinkNITT backend...
uvicorn app.main:app --reload
pause