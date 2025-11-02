# 📱 SMS Forwarding Setup Guide

## 🎯 What You'll Achieve

Real SMS messages from your phone will automatically appear in your SmartSense Inbox web app!

---

## 📋 Prerequisites Checklist

- ✅ Backend running on localhost:8000
- ✅ Frontend running on localhost:4200
- 📱 Android phone with internet connection
- 📱 "Forward SMS to HTTP" app from Play Store

---

## 🚀 Step-by-Step Setup

### Step 1: Start ngrok (Get Public URL)

**In a new terminal (Terminal 3):**

```powershell
cd c:\college\Projects\SmartSense-Inbox-1
.\start-ngrok.ps1
```

**You'll see output like this:**

```
ngrok

Session Status                online
Account                       Your Name (Plan: Free)
Version                       3.x.x
Region                        United States (us)
Latency                       45ms
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123xyz.ngrok.io -> http://localhost:8000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**📝 IMPORTANT: Copy the "Forwarding" URL!**

Example: `https://abc123xyz.ngrok.io`

This is your **public URL** that your phone will use.

---

### Step 2: Install SMS Forwarder App

**On your Android phone:**

1. Open **Google Play Store**
2. Search for **"SMS to URL - Forward SMS to HTTP"**
3. Install the app (by Bogdan Mihai Constantin or similar)
4. Open the app and grant SMS permissions

---

### Step 3: Configure the App

**In the SMS Forwarder app:**

1. **Tap "Add New Forward"** or **"+"** button

2. **Configure these settings:**

   - **Name:** SmartSense Inbox

   - **URL:** `https://YOUR-NGROK-URL.ngrok.io/api/v1/sms`

     Example: `https://abc123xyz.ngrok.io/api/v1/sms`

   - **Method:** POST

   - **Content-Type:** application/json

   - **Body/Payload:** Use this JSON template:
     ```json
     {
       "sender": "{from}",
       "body": "{body}",
       "timestamp": "{sentStamp}",
       "message_id": "{id}"
     }
     ```

3. **Advanced Settings (if available):**

   - Enable: Forward all messages
   - Enable: Auto-start on boot
   - Disable: Only forward when charging (for testing)

4. **Save** the configuration

---

### Step 4: Test the Setup

**Option A: Send yourself a test SMS**

1. From another phone, send an SMS to your phone:

   ```
   From: TESTBANK
   Message: Your account has been credited with Rs.1000. Balance: Rs.5000
   ```

2. Within seconds, you should see:
   - ✅ The SMS appears in your backend terminal logs
   - ✅ The message shows up in your frontend Inbox
   - ✅ It's automatically categorized as "Finance"

**Option B: Use the app's test feature**

1. In the SMS Forwarder app, tap on your configuration
2. Look for "Test" or "Send Test" button
3. It will send a sample message to your backend

---

### Step 5: Verify in Your App

**Check the frontend (http://localhost:4200):**

1. Go to the **Inbox** page
2. You should see your new SMS appear automatically!
3. Check the category - it should be auto-categorized
4. If it contains threats, it will be flagged

**Check the backend terminal:**

You should see logs like:

```
INFO: 127.0.0.1:xxxxx - "POST /api/v1/sms HTTP/1.1" 200 OK
```

---

## 🔍 Troubleshooting

### Phone can't reach the URL

**Problem:** SMS Forwarder shows "Connection failed"

**Solution:**

1. Make sure ngrok is running (Terminal 3)
2. Check the ngrok URL is correct (copy it fresh)
3. Ensure your phone has internet (WiFi or mobile data)
4. Test the URL in your phone's browser first

### Messages not appearing in frontend

**Problem:** Backend receives SMS but frontend doesn't update

**Solution:**

1. Refresh the frontend page (F5)
2. Check the date filter in Inbox - set to "Today"
3. Clear any category filters

### ngrok session expired

**Problem:** ngrok shows "Session Expired"

**Solution:**

1. Free ngrok sessions last 2 hours
2. Restart ngrok: Ctrl+C, then `.\start-ngrok.ps1`
3. Update the URL in your SMS Forwarder app
4. Or sign up for free ngrok account for longer sessions

### Backend not receiving data

**Problem:** No logs in backend terminal

**Solution:**

1. Check backend is running on port 8000
2. Verify the URL format: `https://YOUR-URL.ngrok.io/api/v1/sms`
3. Check the JSON payload format matches exactly
4. Look at ngrok web interface: http://127.0.0.1:4040 for request details

---

## 📊 Expected Behavior

**When an SMS arrives:**

```
1. Phone receives SMS
   ↓ (< 1 second)
2. Forwarder app sends HTTP POST to ngrok URL
   ↓
3. ngrok forwards to localhost:8000
   ↓
4. Backend processes SMS:
   - Extracts sender, body, timestamp
   - Categorizes (OTP, Finance, Offers, etc.)
   - Detects threats (phishing, scams)
   - Extracts URLs
   ↓
5. Saves to database
   ↓
6. Frontend shows new message (refresh to see)
```

---

## 🎯 Demo Tips

**For the hackathon:**

1. **Before Demo:**

   - Have ngrok running (stable URL)
   - Have SMS Forwarder configured and tested
   - Have sample messages ready

2. **During Demo:**

   - Show the Inbox with existing messages
   - Have someone send you a banking SMS
   - Watch it appear in real-time
   - Show the AI categorization
   - Show threat detection if applicable

3. **Backup Plan:**
   - If live SMS fails, use `load-more-sample-data.ps1`
   - Demonstrate with pre-loaded messages
   - Explain the forwarding concept verbally

---

## 🔗 Quick Reference

**URLs:**

- Frontend: http://localhost:4200
- Backend API: http://localhost:8000/docs
- ngrok Inspector: http://127.0.0.1:4040

**Endpoints:**

- Ingest SMS: POST `/api/v1/sms`
- Get Messages: GET `/api/v1/messages`
- Get Digest: GET `/api/v1/digest?date_filter=2025-11-01`

**SMS Forwarder Payload:**

```json
{
  "sender": "{from}",
  "body": "{body}",
  "timestamp": "{sentStamp}",
  "message_id": "{id}"
}
```

---

## ✅ Success Checklist

Before hackathon demo:

- [ ] ngrok running and stable
- [ ] ngrok URL copied
- [ ] SMS Forwarder app installed
- [ ] Forwarder configured with correct URL
- [ ] Test SMS sent successfully
- [ ] Message appeared in frontend
- [ ] Auto-categorization working
- [ ] Threat detection working
- [ ] Phone fully charged
- [ ] Backup plan ready (load-more-sample-data.ps1)

---

**You're ready to impress the judges with real-time SMS processing! 🚀**
