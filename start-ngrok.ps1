# Start ngrok tunnel
Write-Host "Starting ngrok tunnel..." -ForegroundColor Green
Write-Host "Make sure backend is running on port 8000" -ForegroundColor Yellow
ngrok http 8000
