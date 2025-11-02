# SmartSense Inbox - Intelligent SMS Summarizer

**Hackathon Project: Transform SMS chaos into clean, smart summaries**

## 🎯 Overview

SmartSense Inbox is a web-based intelligent SMS management system that:

- Automatically categorizes promotional SMS messages
- Generates daily digests with category breakdowns
- Detects and flags potential threats (phishing, scams)
- Provides natural language Q&A about your messages
- Works with real SMS via forwarder app OR simulated data

## 🏗️ Architecture

- **Backend**: FastAPI (Python) - Processing, classification, and API
- **Frontend**: Angular 20 - User interface
- **Database**: SQLite (lightweight, file-based)
- **AI/ML**: Rule-based classification + Optional OpenAI for chat
- **SMS Integration**: SMS forwarder app + ngrok tunnel

## 📋 Prerequisites

### Required

- Python 3.8+ ([Download](https://www.python.org/downloads/))
- Node.js 18+ and npm ([Download](https://nodejs.org/))
- ngrok account and CLI ([Download](https://ngrok.com/download))
- Android phone with SMS (for real SMS forwarding)

### Optional

- OpenAI API key (for enhanced chat responses)

## 🚀 Quick Start (12-hour Setup)

### Step 1: Clone and Setup Backend (30 min)

```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Edit .env and set your values (optional OpenAI key)
```

### Step 2: Setup Frontend (20 min)

```powershell
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Build and run
npm start
```

### Step 3: Run the Application (5 min)

**Terminal 1 - Backend:**

```powershell
.\start-backend.ps1
```

**Terminal 2 - Frontend:**

```powershell
.\start-frontend.ps1
```

**Terminal 3 - ngrok (for real SMS):**

```powershell
.\start-ngrok.ps1
```

### Step 4: Configure SMS Forwarder (30-60 min)

#### Option A: Use SMS Forwarder App (Recommended)

1. **Install SMS Forwarder App**
   - Open Play Store on Android
   - Search: "SMS Forwarder" or "SMS to HTTP"
   - Recommended apps:
     - "SMS Forwarder" by Asprilo
     - "SMS Forward" by Simple Tools
2. **Grant Permissions**
   - Allow SMS read permission
   - Allow background running
3. **Configure Webhook**
   - Get your ngrok URL from Terminal 3 (e.g., `https://abc123.ngrok-free.app`)
   - In forwarder app, set:
     - URL: `https://YOUR-NGROK-URL.ngrok-free.app/api/v1/sms`
     - Method: POST
     - Content-Type: application/json
     - JSON mapping:
       ```json
       {
         "sender": "{{sender}}",
         "body": "{{body}}",
         "timestamp": "{{timestamp}}"
       }
       ```
4. **Test**
   - Send a test SMS to your phone
   - Check backend terminal for incoming POST
   - Check frontend inbox for new message

#### Option B: Fallback - Upload Sample Data (10 min)

If forwarder doesn't work, use the included sample data:

**Via API (Postman/curl):**

```powershell
# Navigate to sample_data folder
cd sample_data

# Use Python to upload CSV
python upload_sample.py
```

**Or create `upload_sample.py`:**

```python
import csv
import requests
from datetime import datetime

with open('sms_sample.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    messages = []
    for row in reader:
        messages.append({
            'sender': row['sender'],
            'body': row['body'],
            'timestamp': row['timestamp']
        })

response = requests.post('http://localhost:8000/api/v1/upload-csv', json=messages)
print(response.json())
```

## 📱 Expected Webhook JSON Format

The SMS forwarder app should send JSON in this format:

```json
{
  "sender": "HDFCBK",
  "body": "Your A/c XX1234 debited with Rs.5000. Available balance: Rs.45000",
  "timestamp": "2025-10-31T09:15:00Z"
}
```

**Field mapping in forwarder app:**

- `sender` → SMS sender/from field
- `body` → SMS message text
- `timestamp` → SMS received time (ISO format preferred)

## 🎯 Features Demonstration

### 1. View Inbox

- Navigate to `http://localhost:4200/inbox`
- See all messages with categories and threat flags
- Filter by date, category, or threats only

### 2. View Daily Digest

- Navigate to `http://localhost:4200/summary`
- See categorized breakdown (offers, finance, travel, OTP, etc.)
- View threat statistics

### 3. Ask Natural Language Questions

- In Summary page, use the chat box
- Examples:
  - "How many OTP messages?"
  - "Show me banking alerts"
  - "Summarize today's offers"
  - "Any threats detected?"

## 🛠️ API Endpoints

### POST /api/v1/sms

Ingest a single SMS message

```json
{
  "sender": "string",
  "body": "string",
  "timestamp": "2025-10-31T10:00:00Z"
}
```

### GET /api/v1/messages

Get filtered messages

- Query params: `date_filter`, `category`, `threats_only`

### GET /api/v1/digest

Get daily digest

- Query params: `date_filter`

### POST /api/v1/query

Natural language query

```json
{
  "query": "How many offers today?",
  "date": "2025-10-31"
}
```

### POST /api/v1/upload-csv

Bulk upload (fallback)

```json
[
  {
    "sender": "...",
    "body": "...",
    "timestamp": "..."
  }
]
```

## 📊 Categories

Messages are auto-categorized into:

- **OTP**: Verification codes
- **Finance**: Banking, transactions, bills
- **Offers**: Discounts, deals, cashback
- **Travel**: Flight, hotel, train bookings
- **Transactional**: Orders, deliveries
- **Promotional**: General marketing

## 🛡️ Threat Detection

Flags messages with:

- Suspicious shortened URLs (bit.ly, tinyurl, etc.)
- Money transfer requests
- Account impersonation patterns
- Suspicious sender IDs

## 🧪 Testing

### Test with Sample Data

```powershell
# Load 50 sample messages
python sample_data/upload_sample.py
```

### Test Individual Endpoints

```powershell
# Test ingest
curl -X POST http://localhost:8000/api/v1/sms -H "Content-Type: application/json" -d "{\"sender\":\"TEST\",\"body\":\"Test message\"}"

# Test messages
curl http://localhost:8000/api/v1/messages

# Test digest
curl http://localhost:8000/api/v1/digest
```

## 🐛 Troubleshooting

### Backend won't start

- Check Python version: `python --version` (need 3.8+)
- Activate venv: `.\venv\Scripts\Activate.ps1`
- Reinstall deps: `pip install -r requirements.txt`

### Frontend won't start

- Check Node version: `node --version` (need 18+)
- Clear cache: `npm cache clean --force`
- Reinstall: `rm -rf node_modules; npm install`

### ngrok tunnel issues

- Login to ngrok: `ngrok config add-authtoken YOUR_TOKEN`
- Check if port 8000 is used: `netstat -ano | findstr :8000`

### SMS forwarder not sending

- Check phone internet connection
- Verify ngrok URL is correct and HTTPS
- Check app has SMS permission
- Look for firewall blocking ngrok
- Try sending test SMS and check app logs

### No messages in frontend

- Check backend is running: `http://localhost:8000/`
- Check CORS settings in backend
- Open browser console for errors
- Verify API calls in Network tab

## 🎥 Demo Script

1. **Show Empty State**: Open frontend, show no messages
2. **Simulate SMS Arrival**:
   - Send test SMS to phone (forwarder active)
   - OR run upload script
3. **Show Inbox**: Refresh, show categorized message with tags
4. **Show Digest**: Navigate to summary, show stats and breakdown
5. **Demo Chat**: Ask "How many offers?" and show response
6. **Show Threat**: Point out flagged scam message with warning banner

## 📈 Future Enhancements

- Multi-language support
- On-device ML models
- OEM integration
- WhatsApp/email integration
- Advanced personalization

## 👥 Team & Contact

Developed for hackathon demo.

## 📄 License

MIT License - Free to use and modify.

---

## ⏱️ Time Breakdown (12 hours)

- Backend setup: 2 hours
- Frontend setup: 2 hours
- SMS forwarder config: 1 hour
- Testing & debugging: 2 hours
- Sample data & polish: 1 hour
- Documentation: 1 hour
- **Buffer**: 3 hours

**Good luck with your hackathon! 🚀**
