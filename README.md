# SmartSense Inbox - Intelligent SMS Summarizer

**Hackathon Project**: Transform SMS chaos into clean, smart summaries with AI-powered categorization and threat detection.

## 🎯 What is SmartSense Inbox?

# SmartSense Inbox 📱

An intelligent SMS summarizer application built for hackathons. This app helps users manage SMS overload by automatically categorizing messages, detecting threats, generating daily digests, and answering natural language queries about their messages.

## ✅ Status: Functional Demo (In Development)

**Backend**: FastAPI + Google Firestore + Python 3.13  
**Frontend**: Angular 20 + TypeScript  
**Demo Ready**: ✅ Core features are working! See "Features" section for details.

> **Note**: This project is a proof-of-concept. While the core summarization and categorization features are functional using sample data, real-time SMS forwarding is still under development.

## 🚀 Quick Start

### For Hackathon Demo (< 1 day setup)

**See [SETUP_GUIDE.md](SETUP_GUIDE.md) for complete instructions**

#### 1. Backend Setup (30 min)

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

### Frontend Setup

```powershell
# Start the frontend (runs on http://localhost:4200)
.\start-frontend.ps1
```

The frontend will automatically:

- Open browser at http://localhost:4200
- Hot reload on code changes
- Connect to backend API

#### 3. Run Application

```powershell
# Terminal 1 - Backend
.\start-backend.ps1

# Terminal 2 - Frontend
.\start-frontend.ps1

# Terminal 3 - ngrok (for real SMS)
.\start-ngrok.ps1
```

#### 4. Load Sample Data (Quick Demo)

```powershell
cd sample_data
python upload_sample.py
```

**Then open**: http://localhost:4200

## 🌟 Features

### ✅ 1. Smart Categorization (WORKING)

Automatically categorizes SMS into 6 categories using an **LLM (Large Language Model)**:

- 💰 **Finance** - Banking alerts, credit card transactions, payments
- 🎁 **Offers** - Discounts, cashback, promotional deals
- ✈️ **Travel** - Flight bookings, hotel confirmations, PNR details
- 🔐 **OTP** - One-time passwords, verification codes
- 📦 **Transactional** - Order confirmations, delivery updates
- 📢 **Promotional** - Marketing messages, newsletters

**UI Features:**

- Color-coded category badges
- Filter messages by category
- Visual category icons

### 🚧 2. Threat Detection (PARTIALLY IMPLEMENTED)

Identifies potential security threats within messages. The backend service is implemented, but the frontend UI does not yet display threat warnings.

- Suspicious URLs (bit.ly, tinyurl, etc.)
- Money transfer requests
- Account impersonation
- Phishing patterns

### ✅ 3. Daily Digest (WORKING)

Beautiful summary page with:

- 📊 **Overview Stats**: Total messages, categories count, threats detected

### ⏳ 4. SMS Forwarding (IN PROGRESS)

The system is designed to receive SMS from an Android device via a forwarding app. The backend endpoint is ready, but the end-to-end integration is not yet complete.

- **See [SMS_FORWARDING_GUIDE.md](SMS_FORWARDING_GUIDE.md) for setup instructions.**
- Currently, the demo relies on loading sample data.

## 🛣️ What's Next?

- **Complete SMS Forwarding**: Finalize and test the real-time SMS forwarding feature.
- **Threat UI**: Display threat detection warnings in the user interface.
- **Natural Language Query**: Implement a feature to allow users to ask questions about their messages (e.g., "What was the OTP from my bank?").
- **User Authentication**: Add user accounts to support multiple users securely.
- 📂 **Category Breakdown**: Count and summary for each category
- 📅 **Date Filtering**: View digest for any date
- 🎨 **Visual Design**: Stats cards with icons and colors

**API Endpoint**: `GET /api/v1/digest?date_filter=YYYY-MM-DD`

### 4. Natural Language Chat

### ⚡ 4. Natural Language Q&A (READY)

AI-powered chat interface (requires OpenAI API key):

- 💬 Ask questions in plain English
- 🎯 Context-aware responses
- 📝 Example queries built-in

**Examples:**

- "How many OTP messages did I receive?"
- "Show me banking alerts from today"
- "Any suspicious messages?"
- "Summarize my offers"

**Setup**: Add `OPENAI_API_KEY` to `backend/.env`  
**API Endpoint**: `POST /api/v1/query`

## 🏗️ Architecture

**Frontend**: Angular 20  
**Backend**: FastAPI (Python)  
**Database**: SQLite  
**AI/ML**: Rule-based + Optional OpenAI  
**SMS Integration**: SMS Forwarder App + ngrok

## 📱 SMS Integration Options

### Option A: Real SMS (via Forwarder App)

1. Install SMS Forwarder from Play Store
2. Configure webhook to ngrok URL
3. Grant SMS permissions
4. Receive real messages automatically

### Option B: Simulated Data (Fastest)

1. Use included sample CSV (50 messages)
2. Run upload script
3. Demo ready in minutes

**See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions**

## 🎥 Demo Flow

1. **Inbox View**: See categorized messages with threat flags
2. **Daily Digest**: View stats and category breakdown
3. **Chat/Query**: Ask natural language questions
4. **Threat Demo**: Show flagged scam messages

## 📋 Project Structure

```
SmartSense-Inbox/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry
│   │   ├── api/v1/endpoints/    # API routes
│   │   ├── services/            # Business logic
│   │   │   ├── sms_processor.py # Classification & threats
│   │   │   └── llm_client.py    # Optional AI chat
│   │   ├── models/              # Database models
│   │   └── schemas/             # Pydantic schemas
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/app/
│   │   ├── components/
│   │   │   ├── inbox/           # Message list
│   │   │   └── summary/         # Digest & chat
│   │   ├── services/            # API clients
│   │   └── models/              # TypeScript interfaces
│   └── package.json
├── sample_data/
│   ├── sms_sample.csv           # 50 sample messages
│   └── upload_sample.py         # Upload script
├── SETUP_GUIDE.md               # Detailed setup
└── README.md                    # This file
```

## 🛠️ Tech Stack

- **Frontend**: Angular 20, TypeScript, CSS
- **Backend**: FastAPI, Python 3.8+, SQLAlchemy
- **Database**: SQLite (file-based, no setup)
- **AI/ML**:
  - Rule-based classification (keywords, regex)
  - Optional OpenAI for enhanced chat
- **Tools**: ngrok, SMS Forwarder app2. Navigate to the frontend directory and install dependencies:
  ```
  cd frontend
  npm install
  ```

3. Navigate to the backend directory and install dependencies:
   ```
   cd backend
   pip install -r requirements.txt
   ```

## 🧪 API Endpoints

**Base URL**: `http://localhost:8000`

- `POST /api/v1/sms` - Ingest single SMS
- `GET /api/v1/messages` - Get filtered messages
- `GET /api/v1/digest` - Get daily digest
- `POST /api/v1/query` - Natural language Q&A
- `POST /api/v1/upload-csv` - Bulk upload (fallback)

## 🐛 Troubleshooting

**Backend won't start**

- Check Python version: `python --version` (need 3.8+)
- Activate venv: `.\venv\Scripts\Activate.ps1`

**Frontend won't start**

- Check Node version: `node --version` (need 18+)
- Run: `npm install`

**No messages showing**

- Check backend is running: http://localhost:8000
- Check browser console for errors
- Upload sample data: `python sample_data/upload_sample.py`

**SMS forwarder not working**

- Verify ngrok URL is correct
- Check phone has internet
- Grant SMS permissions to app
- Use fallback: upload sample CSV

## 📝 License

MIT License - Free to use and modify

## 👥 Contact

Developed for hackathon demonstration

---

**For complete setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)**

### Docker

To run the application using Docker, use the following command:

```
docker-compose up
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
