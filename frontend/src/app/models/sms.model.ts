export interface Sms {
  id: number;
  sender: string;
  body: string;
  timestamp: Date | string;
  category?: string;
  is_threat: boolean;
  threat_reason?: string;
  urls?: string[];
  has_money_request: boolean;
  has_otp: boolean;
}

export interface CategoryDigest {
  category: string;
  count: number;
  summary: string;
}

export interface DigestResponse {
  date: string;
  total_messages: number;
  categories: CategoryDigest[];
  threat_count: number;
}

export interface QueryResponse {
  answer: string;
  sources?: number[];
}
