# Run Backend Server
Write-Host "Starting SmartSense Inbox Backend..." -ForegroundColor Green
cd backend
$env:PYTHONPATH = $PWD
py -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
