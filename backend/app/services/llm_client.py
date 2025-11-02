from typing import List, Optional
import requests
import json
from app.core.config import settings
from app.models.sms_model import SMS

class LLMClient:
    """LLM client using OpenRouter's AI models"""
    
    def __init__(self):
        # Check for OpenRouter API key
        self.enabled = settings.openai_api_key is not None
        self.api_key = settings.openai_api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        # Multiple free models for better availability
        self.models = [
            "deepseek/deepseek-r1:free",           # Primary: DeepSeek R1 (best reasoning)
            "google/gemini-2.0-flash-exp:free",    # Fallback 1: Gemini Flash (fast)
            "meta-llama/llama-3.2-3b-instruct:free", # Fallback 2: Llama 3.2 (reliable)
            "qwen/qwen-2-7b-instruct:free",        # Fallback 3: Qwen 2 (good quality)
        ]
    
    def answer_query(self, query: str, messages: List[SMS]) -> str:
        """Answer a natural language query about messages using AI"""
        if not self.enabled:
            print("⚠️ LLM disabled - using fallback (API key not configured)")
            return self._fallback_answer(query, messages)
        
        # Try all models in order until one succeeds
        for i, model in enumerate(self.models):
            if i > 0:
                print(f"🔄 Trying fallback model {i}: {model}")
            
            result = self._call_llm(query, messages, model)
            if result:
                return result
        
        # If all models fail, use rule-based fallback
        print("↩️ All AI models unavailable, using rule-based answer")
        return self._fallback_answer(query, messages)
    
    def _call_llm(self, query: str, messages: List[SMS], model: str) -> Optional[str]:
        """Call LLM API with specified model"""
        try:
            print(f"🤖 Calling {model} for query: '{query}'")
            print(f"📊 Context: {len(messages)} messages")
            
            # Prepare context
            context = self._prepare_context(messages)
            
            prompt = f"""You are an SMS assistant. Answer the user's question based on their SMS messages.

Messages context:
{context}

User question: {query}

Provide a concise, helpful answer."""

            # Use OpenRouter API
            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:4200",
                    "X-Title": "SmartSense Inbox",
                },
                json={
                    "model": model,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result['choices'][0]['message']['content'].strip()
                print(f"✅ {model} responded successfully")
                return answer
            elif response.status_code == 429:
                print(f"⏳ {model} is rate-limited")
                return None
            else:
                print(f"❌ API error ({response.status_code}): {response.text[:200]}")
                return None
        
        except Exception as e:
            print(f"❌ Error with {model}: {e}")
            return None

    
    def generate_summary(self, category: str, messages: List[SMS]) -> str:
        """Generate an abstractive summary for a category"""
        if not self.enabled or len(messages) == 0:
            return f"{len(messages)} {category} messages"
        
        try:
            # Sample first few messages
            sample = messages[:5]
            bodies = "\n".join([f"- {msg.body[:100]}" for msg in sample])
            
            prompt = f"""Summarize these {category} SMS messages in one concise line (max 15 words):

{bodies}

Summary:"""

            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "max_tokens": 50,
                    "temperature": 0.5
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                return f"{len(messages)} {category} messages"
        
        except Exception:
            return f"{len(messages)} {category} messages"
    
    def _prepare_context(self, messages: List[SMS], max_messages: int = 20) -> str:
        """Prepare message context for LLM"""
        lines = []
        for i, msg in enumerate(messages[:max_messages]):
            date_str = msg.timestamp.strftime("%Y-%m-%d %H:%M")
            lines.append(f"{i+1}. From: {msg.sender} | {date_str} | Category: {msg.category}")
            lines.append(f"   Message: {msg.body[:150]}")
        
        if len(messages) > max_messages:
            lines.append(f"\n... and {len(messages) - max_messages} more messages")
        
        return "\n".join(lines)
    
    def _fallback_answer(self, query: str, messages: List[SMS]) -> str:
        """Rule-based fallback when LLM unavailable"""
        query_lower = query.lower()
        
        # Count queries
        if any(word in query_lower for word in ['how many', 'count', 'number of']):
            if 'otp' in query_lower:
                count = sum(1 for m in messages if m.category == 'otp')
                return f"You have {count} OTP messages."
            elif 'offer' in query_lower:
                count = sum(1 for m in messages if m.category == 'offers')
                return f"You have {count} offer messages."
            elif 'bank' in query_lower or 'finance' in query_lower:
                count = sum(1 for m in messages if m.category == 'finance')
                return f"You have {count} banking messages."
            elif 'threat' in query_lower or 'scam' in query_lower:
                count = sum(1 for m in messages if m.is_threat)
                return f"You have {count} potential threat messages flagged."
            else:
                return f"You have {len(messages)} total messages."
        
        # Show queries
        if 'show' in query_lower or 'list' in query_lower:
            if 'otp' in query_lower:
                otps = [m for m in messages if m.has_otp][:5]
                if otps:
                    result = "Recent OTP messages:\n"
                    for msg in otps:
                        result += f"- From {msg.sender}: {msg.body[:80]}\n"
                    return result
                return "No OTP messages found."
            elif 'threat' in query_lower:
                threats = [m for m in messages if m.is_threat][:5]
                if threats:
                    result = "Flagged threat messages:\n"
                    for msg in threats:
                        result += f"- From {msg.sender}: {msg.threat_reason}\n"
                    return result
                return "No threats detected."
        
        # Summarize queries
        if 'summarize' in query_lower or 'summary' in query_lower:
            categories = {}
            for msg in messages:
                cat = msg.category or 'other'
                categories[cat] = categories.get(cat, 0) + 1
            
            parts = [f"{count} {cat}" for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)]
            return f"Summary: {', '.join(parts)}"
        
        return f"I found {len(messages)} messages. Try asking 'how many offers' or 'show OTPs' or 'summarize today'."

# Singleton instance
llm_client = LLMClient()
