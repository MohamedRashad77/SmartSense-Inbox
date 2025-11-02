# Load 100 additional simulated SMS messages for today
# Requires backend running at http://localhost:8000

param(
    [string]$ApiBase = "http://localhost:8000",
    [string]$Date = (Get-Date -Format "yyyy-MM-dd")
)

Write-Host "Adding 100 simulated SMS messages for $Date..." -ForegroundColor Cyan

$endpoint = "$ApiBase/api/v1/sms"

# Helper: ISO timestamp for given hour/minute
function New-TimeStamp {
    param(
        [string]$date,
        [int]$hour,
        [int]$minute
    )
    $time = ("{0}:{1}:00" -f $hour, $minute)
    $dt = "$date $time"
    return [datetime]::ParseExact($dt, "yyyy-MM-dd H:m:s", $null).ToString("o")
}

# Pools of realistic content
$names = @("Mom","Dad","Rahul","Priya","Sandeep","Anita","Karthik","Neha","Akash","Vikram","Aisha","Shreya","Rohan","Ishita","Varun","Arjun","Deepa","Kiran","Sameer","Meera")
$personalTexts = @(
    "Hey, reached safely. Call me when free.",
    "Dinner at 8? Shall I book a table?",
    "Where are you? I'm waiting downstairs.",
    "Don't forget to bring the documents tomorrow.",
    "Happy Birthday! Have an amazing day!",
    "Traffic is crazy. Will be 15 mins late.",
    "Sent you the photos on WhatsApp.",
    "Meeting got postponed to Monday.",
    "Doctor appointment confirmed for 5 PM.",
    "Call me when you see this.",
    "EMI reminder came, please check once.",
    "Shall we go trekking next weekend?",
    "Interview went well! Fingers crossed.",
    "Please pick up milk on your way.",
    "WiFi not working, can you restart router?"
)

$interviewTexts = @(
    "Interview scheduled for 11:30 AM tomorrow. Join: https://meet.google.com/abc-defg-hij",
    "Your profile shortlisted. Zoom link: https://zoom.us/j/9345123456 Passcode: 927351",
    "Coding round at 6 PM today. HackerRank link: https://www.hackerrank.com/test/xyz",
    "HR from AcmeCorp: Please confirm availability for discussion. Teams: https://teams.microsoft.com/l/meetup-join/19%3ameeting",
    "Reminder: Tech interview at 3 PM. JD attached. Meet: https://meet.google.com/qwe-rtas-yui"
)

$financeTexts = @(
    "HDFC BANK: INR 5000 debited from A/C XXXX1234. Avl Bal INR 45,000. If not you, call 1800-xxx.",
    "SBI: Rs.2500 spent on your Credit Card at AMAZON. SMS BLOCK if not done by you.",
    "PAYTM: Rs.1500 cashback credited. Wallet balance Rs.2500.",
    "ICICI BANK: Salary Rs.62,500 credited to A/C ****8910. Avl bal Rs.1,24,300.",
    "UPI: Rs.799 paid to ZOMATO via UPI Ref 123456789012"
)

$otpTexts = @(
    "Your OTP is 482913 for login. Do not share.",
    "Use 927351 as OTP to verify your number.",
    "OTP 663920 for transaction of Rs.2500. Valid for 10 mins.",
    "Do not share this code: 118244",
    "Verification code: 560091"
)

$offerTexts = @(
    "FLIPKART: Big Billion Days! Up to 80% OFF on electronics. Shop now.",
    "ZOMATO: Flat 60% OFF this weekend. Use code ZM60.",
    "SWIGGY: 50% OFF on your next order. Use code SAVE50.",
    "MYNTRA: Upto 70% SALE live now!",
    "AJIO: Flat Rs.500 OFF on Rs.1999+ | Code AJ500"
)

$travelTexts = @(
    "IRCTC: PNR 6512347890 CONFIRMED. Train departs 18:40 from SBC.",
    "MakeMyTrip: Flight 6E-123 to DEL at 07:15, Web check-in open.",
    "GOIBIBO: Hotel booking CONFIRMED, Check-in 2 PM today.",
    "Uber: Your ride with Ravi arrives in 3 mins.",
    "RedBus: Boarding point updated. Bus at 10:20 PM."
)

$transactionalTexts = @(
    "AMAZON: Your order #171-123 delivered. Rate your experience.",
    "FLIPKART: Order dispatched. Tracking ID: FK123456789.",
    "SWIGGY: Order confirmed. Arriving in 26 mins.",
    "ZOMATO: Delivery partner picked up your order.",
    "NYKAA: Order packed and ready to ship."
)

$threatTexts = @(
    "Dear customer, your account will be blocked. Verify now: http://bit.ly/verify-acc",
    "URGENT: KYC expired. Update details at http://tinyurl.com/kyc-update",
    "Your package is on hold. Pay 49 to release: http://scam.example/pay",
    "Bank Notice: Suspicious login. Click to secure: https://short.ly/secure",
    "ATM card blocked. Reactivate here: http://goo.gl/r3activ8"
)

# Build 100 messages with a balanced distribution
$messages = @()

# 25 personal
1..25 | ForEach-Object {
    $from = $names[(Get-Random -Minimum 0 -Maximum $names.Count)]
    $body = $personalTexts[(Get-Random -Minimum 0 -Maximum $personalTexts.Count)]
    $h = Get-Random -Minimum 8 -Maximum 22
    $m = Get-Random -Minimum 0 -Maximum 59
    $messages += [PSCustomObject]@{ sender=$from; body=$body; timestamp=(New-TimeStamp -date $Date -hour $h -minute $m) }
}

# 12 interview / meeting links
1..12 | ForEach-Object {
    $from = "HR-" + ("Acme","Innotech","Globex","Soylent","Umbrella","Stark","Wayne" | Get-Random)
    $body = $interviewTexts[(Get-Random -Minimum 0 -Maximum $interviewTexts.Count)]
    $h = Get-Random -Minimum 9 -Maximum 20
    $m = Get-Random -Minimum 0 -Maximum 59
    $messages += [PSCustomObject]@{ sender=$from; body=$body; timestamp=(New-TimeStamp -date $Date -hour $h -minute $m) }
}

# 18 finance
1..18 | ForEach-Object {
    $from = ("HDFC-BANK","SBI-BANK","ICICI-BANK","AXIS-BANK","KOTAK") | Get-Random
    $body = $financeTexts[(Get-Random -Minimum 0 -Maximum $financeTexts.Count)]
    $h = Get-Random -Minimum 0 -Maximum 23
    $m = Get-Random -Minimum 0 -Maximum 59
    $messages += [PSCustomObject]@{ sender=$from; body=$body; timestamp=(New-TimeStamp -date $Date -hour $h -minute $m) }
}

# 8 OTP
1..8 | ForEach-Object {
    $from = ("OTPVERIFY","AMAZN-OTP","PAYTM-OTP","GMAIL-VERIF") | Get-Random
    $body = $otpTexts[(Get-Random -Minimum 0 -Maximum $otpTexts.Count)]
    $h = Get-Random -Minimum 0 -Maximum 23
    $m = Get-Random -Minimum 0 -Maximum 59
    $messages += [PSCustomObject]@{ sender=$from; body=$body; timestamp=(New-TimeStamp -date $Date -hour $h -minute $m) }
}

# 12 offers
1..12 | ForEach-Object {
    $from = ("FLIPKART","ZOMATO","SWIGGY","MYNTRA","AJIO","NYKAA") | Get-Random
    $body = $offerTexts[(Get-Random -Minimum 0 -Maximum $offerTexts.Count)]
    $h = Get-Random -Minimum 8 -Maximum 22
    $m = Get-Random -Minimum 0 -Maximum 59
    $messages += [PSCustomObject]@{ sender=$from; body=$body; timestamp=(New-TimeStamp -date $Date -hour $h -minute $m) }
}

# 8 travel
1..8 | ForEach-Object {
    $from = ("IRCTC","MAKEMYTRIP","GOIBIBO","UBER","REDBUS") | Get-Random
    $body = $travelTexts[(Get-Random -Minimum 0 -Maximum $travelTexts.Count)]
    $h = Get-Random -Minimum 5 -Maximum 23
    $m = Get-Random -Minimum 0 -Maximum 59
    $messages += [PSCustomObject]@{ sender=$from; body=$body; timestamp=(New-TimeStamp -date $Date -hour $h -minute $m) }
}

# 10 transactional
1..10 | ForEach-Object {
    $from = ("AMAZN","FLIPKART","SWIGGY","ZOMATO","NYKAA") | Get-Random
    $body = $transactionalTexts[(Get-Random -Minimum 0 -Maximum $transactionalTexts.Count)]
    $h = Get-Random -Minimum 7 -Maximum 23
    $m = Get-Random -Minimum 0 -Maximum 59
    $messages += [PSCustomObject]@{ sender=$from; body=$body; timestamp=(New-TimeStamp -date $Date -hour $h -minute $m) }
}

# 5 threats/scams
1..5 | ForEach-Object {
    $from = ("UNKNOWN","INFO","NOTICE","CARE","SERVICE") | Get-Random
    $body = $threatTexts[(Get-Random -Minimum 0 -Maximum $threatTexts.Count)]
    $h = Get-Random -Minimum 0 -Maximum 23
    $m = Get-Random -Minimum 0 -Maximum 59
    $messages += [PSCustomObject]@{ sender=$from; body=$body; timestamp=(New-TimeStamp -date $Date -hour $h -minute $m) }
}

# Add 2 misc personal to make it 100
1..2 | ForEach-Object {
    $from = $names[(Get-Random -Minimum 0 -Maximum $names.Count)]
    $body = $personalTexts[(Get-Random -Minimum 0 -Maximum $personalTexts.Count)]
    $h = Get-Random -Minimum 8 -Maximum 22
    $m = Get-Random -Minimum 0 -Maximum 59
    $messages += [PSCustomObject]@{ sender=$from; body=$body; timestamp=(New-TimeStamp -date $Date -hour $h -minute $m) }
}

# Sanity: cap in case distribution changes
$messages = $messages | Select-Object -First 100

$success = 0
$fail = 0

for ($i=0; $i -lt $messages.Count; $i++) {
    $msg = $messages[$i]
    $payload = @{ sender=$msg.sender; body=$msg.body; timestamp=$msg.timestamp } | ConvertTo-Json

    try {
        Invoke-RestMethod -Uri $endpoint -Method Post -Body $payload -ContentType "application/json" -TimeoutSec 10
        $success++
        if (($i+1) % 20 -eq 0) { Write-Host "Posted $($i+1)/$($messages.Count)..." -ForegroundColor DarkGray }
    }
    catch {
        $fail++
        Write-Host "Failed #$($i+1): $($msg.sender) - $($msg.body.Substring(0, [Math]::Min(40,$msg.body.Length)))..." -ForegroundColor Red
    }
}

Write-Host ""; Write-Host "Completed. Success: $success, Failed: $fail" -ForegroundColor Green
if ($fail -eq 0) { Write-Host "All messages ingested successfully." -ForegroundColor Green }
