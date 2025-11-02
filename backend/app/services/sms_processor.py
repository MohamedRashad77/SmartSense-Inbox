import re
from typing import List, Dict, Optional
from datetime import datetime
from app.models.sms_model import SMS

class SMSProcessor:
    """Rule-based SMS processor for classification, entity extraction, and threat detection"""
    
    # Category keywords
    CATEGORY_KEYWORDS = {
        'otp': [
            r'\b\d{4,6}\b.*(?:otp|code|verification|verify|password)',
            r'(?:otp|code|verification).*\b\d{4,6}\b',
        ],
        'finance': [
            r'\b(?:bank|account|credit|debit|payment|transaction|balance|rupees?|rs\.?|inr)\b',
            r'\b(?:loan|emi|deposit|withdraw|transfer)\b',
        ],
        'offers': [
            r'\b(?:offer|discount|sale|deal|cashback|coupon|voucher|reward)\b',
            r'\b(?:\d+%\s*off|flat\s*\d+|upto\s*\d+)\b',
        ],
        'travel': [
            r'\b(?:flight|train|bus|hotel|booking|journey|ticket|pnr)\b',
            r'\b(?:irctc|makemytrip|goibibo|cleartrip|redbus)\b',
        ],
        'transactional': [
            r'\b(?:order|delivery|shipped|dispatched|confirmed|receipt)\b',
            r'\b(?:amazon|flipkart|myntra|zomato|swiggy)\b',
        ],
    }
    
    # Threat patterns
    THREAT_PATTERNS = {
        'suspicious_links': [
            r'bit\.ly', r'tinyurl', r'goo\.gl', r't\.co',  # URL shorteners
            r'http[s]?://[^\s]+',  # Generic URLs
        ],
        'money_request': [
            r'\b(?:send|transfer|pay|deposit).*(?:money|amount|rupees?|rs\.?)\b',
            r'\b(?:urgent|immediately|asap).*(?:payment|money)\b',
            r'\bclick.*link.*(?:verify|update|confirm)\b',
        ],
        'impersonation': [
            r'\b(?:your account|account holder|dear customer).*(?:suspended|blocked|locked|expired)\b',
            r'\b(?:update|verify|confirm).*(?:kyc|details|information|account)\b',
        ],
    }
    
    # Suspicious sender patterns
    SUSPICIOUS_SENDERS = [
        r'^[A-Z]{2}-[A-Z]+$',  # Random patterns
        r'^\d{5,}$',  # Long numeric senders
    ]
    
    def classify(self, body: str) -> str:
        """Classify SMS into category"""
        body_lower = body.lower()
        
        # Check OTP first (highest priority)
        for pattern in self.CATEGORY_KEYWORDS['otp']:
            if re.search(pattern, body_lower, re.IGNORECASE):
                return 'otp'
        
        # Check other categories
        category_scores = {}
        for category, patterns in self.CATEGORY_KEYWORDS.items():
            if category == 'otp':
                continue
            score = sum(1 for pattern in patterns if re.search(pattern, body_lower, re.IGNORECASE))
            if score > 0:
                category_scores[category] = score
        
        if category_scores:
            return max(category_scores, key=category_scores.get)
        
        return 'promotional'
    
    def extract_urls(self, body: str) -> List[str]:
        """Extract all URLs from message"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(url_pattern, body)
    
    def detect_threat(self, sender: str, body: str) -> tuple[bool, Optional[str]]:
        """Detect if message is a potential threat"""
        reasons = []
        body_lower = body.lower()
        
        # Check for suspicious links
        urls = self.extract_urls(body)
        for url in urls:
            for pattern in self.THREAT_PATTERNS['suspicious_links']:
                if re.search(pattern, url, re.IGNORECASE):
                    reasons.append("Contains suspicious shortened URL")
                    break
        
        # Check for money request patterns
        for pattern in self.THREAT_PATTERNS['money_request']:
            if re.search(pattern, body_lower, re.IGNORECASE):
                reasons.append("Requests money transfer or urgent payment")
                break
        
        # Check for impersonation patterns
        for pattern in self.THREAT_PATTERNS['impersonation']:
            if re.search(pattern, body_lower, re.IGNORECASE):
                reasons.append("Possible account impersonation or phishing")
                break
        
        # Check suspicious sender
        for pattern in self.SUSPICIOUS_SENDERS:
            if re.match(pattern, sender):
                reasons.append("Suspicious sender ID")
                break
        
        is_threat = len(reasons) > 0
        threat_reason = "; ".join(reasons) if reasons else None
        
        return is_threat, threat_reason
    
    def has_money_request(self, body: str) -> bool:
        """Check if message contains money request"""
        body_lower = body.lower()
        for pattern in self.THREAT_PATTERNS['money_request']:
            if re.search(pattern, body_lower, re.IGNORECASE):
                return True
        return False
    
    def has_otp(self, body: str) -> bool:
        """Check if message contains OTP"""
        for pattern in self.CATEGORY_KEYWORDS['otp']:
            if re.search(pattern, body.lower(), re.IGNORECASE):
                return True
        return False
    
    def process_message(self, sender: str, body: str, timestamp: Optional[datetime] = None) -> Dict:
        """Process a single SMS message"""
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        category = self.classify(body)
        urls = self.extract_urls(body)
        is_threat, threat_reason = self.detect_threat(sender, body)
        
        return {
            'sender': sender,
            'body': body,
            'timestamp': timestamp,
            'category': category,
            'is_threat': is_threat,
            'threat_reason': threat_reason,
            'urls': urls if urls else None,
            'has_money_request': self.has_money_request(body),
            'has_otp': self.has_otp(body),
        }
    
    def generate_digest(self, messages: List[SMS], date: str) -> Dict:
        """Generate daily digest from messages"""
        category_groups = {}
        threat_count = 0
        
        for msg in messages:
            if msg.is_threat:
                threat_count += 1
            
            category = msg.category or 'uncategorized'
            if category not in category_groups:
                category_groups[category] = []
            category_groups[category].append(msg)
        
        # Generate summaries
        categories = []
        for category, msgs in category_groups.items():
            count = len(msgs)
            summary = self._generate_category_summary(category, count, msgs)
            categories.append({
                'category': category,
                'count': count,
                'summary': summary
            })
        
        # Sort by count descending
        categories.sort(key=lambda x: x['count'], reverse=True)
        
        return {
            'date': date,
            'total_messages': len(messages),
            'categories': categories,
            'threat_count': threat_count
        }
    
    def _generate_category_summary(self, category: str, count: int, messages: List[SMS]) -> str:
        """Generate a one-line summary for a category"""
        templates = {
            'offers': f"{count} promotional offers and deals",
            'finance': f"{count} banking and financial updates",
            'travel': f"{count} travel and booking confirmations",
            'otp': f"{count} OTP and verification codes",
            'transactional': f"{count} order and delivery updates",
            'promotional': f"{count} promotional messages",
        }
        
        return templates.get(category, f"{count} {category} messages")

# Singleton instance
sms_processor = SMSProcessor()
