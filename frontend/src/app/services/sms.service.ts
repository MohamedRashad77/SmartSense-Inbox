import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Sms, DigestResponse, QueryResponse } from '../models/sms.model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class SmsService {
  private apiUrl = `${environment.apiBaseUrl}/api/v1`;

  constructor(private http: HttpClient) {}

  // Get messages with optional filters
  getMessages(
    dateFilter?: string,
    category?: string,
    threatsOnly: boolean = false
  ): Observable<Sms[]> {
    let params = new HttpParams();
    if (dateFilter) params = params.set('date_filter', dateFilter);
    if (category) params = params.set('category', category);
    if (threatsOnly) params = params.set('threats_only', 'true');

    return this.http.get<Sms[]>(`${this.apiUrl}/messages`, { params });
  }

  // Get daily digest
  getDigest(dateFilter?: string): Observable<DigestResponse> {
    let params = new HttpParams();
    if (dateFilter) params = params.set('date_filter', dateFilter);

    return this.http.get<DigestResponse>(`${this.apiUrl}/digest`, { params });
  }

  // Query messages with natural language
  queryMessages(query: string, date?: string): Observable<QueryResponse> {
    return this.http.post<QueryResponse>(`${this.apiUrl}/query`, {
      query,
      date,
    });
  }

  // Upload CSV (fallback method)
  uploadCSV(messages: any[]): Observable<any> {
    return this.http.post(`${this.apiUrl}/upload-csv`, messages);
  }

  // Ingest single SMS (for testing)
  ingestSMS(sender: string, body: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/sms`, {
      sender,
      body,
      timestamp: new Date().toISOString(),
    });
  }
}
