# Troubleshooting Guide - SmartSense Inbox

## 🔧 Common Issues & Solutions

### Backend Issues

#### ❌ "Import errors" when starting backend

**Problem**: Module not found errors

```
ImportError: No module named 'fastapi'
```

**Solution**:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

#### ❌ "Port 8000 already in use"

**Problem**: Another process using port 8000

**Solution**:

```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (replace PID with actual number)
taskkill /PID <PID> /F

# Or use different port
python -m uvicorn app.main:app --reload --port 8001
```

---

#### ❌ Database errors

**Problem**: SQLite database locked or corrupted

**Solution**:

```powershell
cd backend
# Backup old database (if needed)
copy sms.db sms.db.backup
# Delete database
rm sms.db
# Restart backend (will recreate)
```

---

#### ❌ "pydantic_settings not found"

**Problem**: Older pydantic version

**Solution**:

```powershell
pip install pydantic-settings
# Or
pip install --upgrade pydantic
```

---

### Frontend Issues

#### ❌ "Cannot find module '@angular/core'"

**Problem**: node_modules not installed

**Solution**:

```powershell
cd frontend
npm install
```

---

#### ❌ "npm ERR! code ENOENT"

**Problem**: npm not found or not in PATH

**Solution**:

1. Verify Node.js installed: `node --version`
2. Reinstall Node.js from https://nodejs.org/
3. Restart terminal

---

#### ❌ Frontend shows blank page

**Problem**: Multiple possible causes

**Solutions**:

```powershell
# 1. Check browser console (F12)
# Look for CORS errors or 404s

# 2. Verify backend is running
curl http://localhost:8000/health

# 3. Check API URL in environment.ts
# Should be: http://localhost:8000

# 4. Clear browser cache
# Ctrl+Shift+R (hard reload)

# 5. Restart frontend
# Ctrl+C, then: npm start
```

---

#### ❌ "ng: command not found"

**Problem**: Angular CLI not installed globally

**Solution**:

```powershell
npm install -g @angular/cli
# Or use npx
npx ng serve
```

---

### ngrok Issues

#### ❌ "ngrok: command not found"

**Problem**: ngrok not installed or not in PATH

**Solution**:

1. Download from https://ngrok.com/download
2. Extract to a folder
3. Add to PATH or use full path:

```powershell
C:\path\to\ngrok.exe http 8000
```

---

#### ❌ "ngrok tunnel failed to connect"

**Problem**: Authentication or connection issue

**Solution**:

```powershell
# Authenticate (get token from ngrok.com)
ngrok config add-authtoken YOUR_AUTH_TOKEN

# Check internet connection
ping ngrok.com

# Try different region
ngrok http 8000 --region=us
```

---

#### ❌ ngrok tunnel URL changes frequently

**Problem**: Free tier assigns random URLs

**Solution**:

- Paid ngrok account gives static subdomain
- For demo: keep terminal open, don't restart
- Update forwarder app URL when it changes

---

### SMS Forwarder Issues

#### ❌ Messages not forwarding

**Problem**: Multiple possible causes

**Solutions**:

1. **Check app permissions**:

   - Go to phone Settings → Apps → SMS Forwarder
   - Ensure SMS permission granted
   - Ensure "Background running" allowed

2. **Check internet connection**:

   - Phone needs WiFi or mobile data
   - Test: open browser, visit google.com

3. **Verify webhook URL**:

   - Should be: `https://YOUR-NGROK-URL.ngrok-free.app/api/v1/sms`
   - Must be HTTPS (ngrok provides this)
   - Must include `/api/v1/sms` path

4. **Check app logs**:

   - Most forwarder apps have logs
   - Look for error messages

5. **Test with curl**:

```powershell
curl -X POST https://YOUR-NGROK-URL.ngrok-free.app/api/v1/sms -H "Content-Type: application/json" -d "{\"sender\":\"TEST\",\"body\":\"Test message\",\"timestamp\":\"2025-10-31T10:00:00Z\"}"
```

---

#### ❌ Wrong JSON format

**Problem**: Forwarder app sends different field names

**Solution**:
Check app's field mapping options. Should map to:

```json
{
  "sender": "{{from}}", // or {{sender}}, {{phone}}
  "body": "{{text}}", // or {{message}}, {{body}}
  "timestamp": "{{date}}" // or {{time}}, {{timestamp}}
}
```

Some apps use different placeholders. Check app documentation.

---

### Data Issues

#### ❌ No messages showing in frontend

**Problem**: Database empty

**Solution**:

```powershell
# Upload sample data
cd sample_data
python upload_sample.py

# Or use API directly
curl http://localhost:8000/api/v1/messages
# Should return JSON array
```

---

#### ❌ Upload script fails

**Problem**: Backend not running or CSV missing

**Solutions**:

1. **Check backend is running**:

```powershell
curl http://localhost:8000/
# Should return welcome message
```

2. **Check CSV file exists**:

```powershell
dir sample_data\sms_sample.csv
# Should show file
```

3. **Check CSV format**:
   First line should be: `sender,body,timestamp`

---

#### ❌ Messages have wrong categories

**Problem**: Classification rules not matching

**Solution**:

1. Check message content - might genuinely be hard to classify
2. Add keywords to `sms_processor.py`:

```python
CATEGORY_KEYWORDS = {
    'your_category': [
        r'keyword1',
        r'keyword2'
    ]
}
```

---

### OpenAI Integration Issues

#### ❌ "OpenAI API key invalid"

**Problem**: Wrong or missing API key

**Solution**:

```powershell
# Edit backend/.env
# Set: OPENAI_API_KEY=sk-...your-key...

# Restart backend
```

---

#### ❌ Chat responses are generic/unhelpful

**Problem**: Falling back to rule-based (OpenAI not configured)

**Solution**:
This is expected! Rule-based fallback works fine for demo.
To use OpenAI:

1. Get API key from https://platform.openai.com/
2. Add to `.env`
3. Restart backend

---

### CORS Issues

#### ❌ "CORS policy" error in browser console

**Problem**: Frontend can't access backend

**Solution**:

1. Backend should already have CORS enabled in `main.py`
2. If not, add:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### Performance Issues

#### ❌ Slow message processing

**Problem**: Processing many messages

**Solution**:

- SQLite is fast for <10,000 messages
- Add database indexes (already included)
- If using OpenAI, it adds 1-3 sec latency (expected)

---

#### ❌ Frontend slow to load

**Problem**: Network or build issue

**Solution**:

```powershell
# Production build (faster)
cd frontend
npm run build
# Serve from dist/ folder
```

---

## 🆘 Emergency Fixes (Demo Day)

### If everything breaks:

**Plan A - Use sample data only**:

```powershell
# Skip SMS forwarder entirely
# Just use: python sample_data/upload_sample.py
# Show the 50 sample messages
```

**Plan B - Show API docs**:

```powershell
# Open: http://localhost:8000/docs
# Show endpoints working with "Try it out"
```

**Plan C - Code walkthrough**:

- Show `sms_processor.py` classification logic
- Explain threat detection patterns
- Show sample CSV data
- Draw architecture on whiteboard

**Plan D - Screenshots**:

- Take screenshots of working app beforehand
- Use as slides if live demo fails

---

## 📞 Quick Diagnostics

Run these commands to check system health:

```powershell
# 1. Check Python
python --version
# Should be 3.8+

# 2. Check Node
node --version
# Should be 18+

# 3. Check backend running
curl http://localhost:8000/health
# Should return {"status":"healthy"}

# 4. Check frontend running
curl http://localhost:4200
# Should return HTML

# 5. Check database
dir backend\sms.db
# Should exist after first run

# 6. Check sample data
python sample_data\upload_sample.py
# Should show success

# 7. Check API
curl http://localhost:8000/api/v1/messages
# Should return JSON array
```

---

## 🔍 Debug Mode

### Enable verbose logging:

**Backend**:
Edit `backend/.env`:

```
DEBUG=True
```

**Frontend**:
Open browser console (F12), check:

- Console tab for errors
- Network tab for API calls
- Response tab to see data

---

## 📝 Log Locations

**Backend logs**:

- Console output (terminal where backend runs)
- Add logging to `backend/app/core/logging.py` if needed

**Frontend logs**:

- Browser console (F12 → Console tab)

**ngrok logs**:

- Terminal where ngrok runs
- Web interface: http://localhost:4040

---

## ✅ Verification Checklist

Before demo, verify:

- [ ] `python check_system.py` passes
- [ ] Backend starts without errors
- [ ] Frontend loads at http://localhost:4200
- [ ] Sample data uploads successfully
- [ ] Inbox shows 50 messages
- [ ] Digest shows statistics
- [ ] Chat returns responses
- [ ] Filters work (category, date, threats)

---

**If all else fails, take a deep breath, explain the concept clearly, and show the code. Judges appreciate honesty and understanding over perfect demos! 🚀**
