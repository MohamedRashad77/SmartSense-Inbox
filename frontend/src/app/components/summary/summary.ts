import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SmsService } from '../../services/sms.service';
import { DigestResponse, CategoryDigest } from '../../models/sms.model';

@Component({
  selector: 'app-summary',
  imports: [CommonModule, FormsModule],
  templateUrl: './summary.html',
  styleUrl: './summary.css',
})
export class Summary implements OnInit {
  digest: DigestResponse | null = null;
  loading: boolean = true;
  selectedDate: string = '';

  queryText: string = '';
  queryResponse: string = '';
  queryLoading: boolean = false;

  constructor(private smsService: SmsService) {
    // Set default date to today
    const today = new Date();
    this.selectedDate = today.toISOString().split('T')[0];
  }

  ngOnInit(): void {
    this.loadDigest();
  }

  loadDigest(): void {
    this.loading = true;
    this.smsService.getDigest(this.selectedDate).subscribe({
      next: (data: DigestResponse) => {
        this.digest = data;
        this.loading = false;
      },
      error: (error) => {
        console.error('Error fetching digest', error);
        this.loading = false;
      },
    });
  }

  onDateChange(): void {
    this.loadDigest();
  }

  askQuery(): void {
    if (!this.queryText.trim()) return;

    this.queryLoading = true;
    this.smsService.queryMessages(this.queryText, this.selectedDate).subscribe({
      next: (response) => {
        this.queryResponse = response.answer;
        this.queryLoading = false;
      },
      error: (error) => {
        console.error('Error querying messages', error);
        this.queryResponse = 'Error processing your query.';
        this.queryLoading = false;
      },
    });
  }

  setQuery(query: string): void {
    this.queryText = query;
  }

  getCategoryNames(): string {
    if (!this.digest || !this.digest.categories.length) return '';
    const topCategories = this.digest.categories
      .slice(0, 3)
      .map((c) => c.category)
      .join(', ');
    return topCategories;
  }

  getThreatStatus(): string {
    if (!this.digest) return '';
    return this.digest.threat_count > 0
      ? `${this.digest.threat_count} suspicious messages`
      : 'All clear!';
  }

  getPercentage(count: number): number {
    if (!this.digest || this.digest.total_messages === 0) return 0;
    return (count / this.digest.total_messages) * 100;
  }

  formatResponse(response: string): string {
    // Add basic formatting to the response
    return response
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n/g, '<br>');
  }

  getCategoryColor(category: string): string {
    const colors: { [key: string]: string } = {
      offers: '#4CAF50',
      finance: '#2196F3',
      travel: '#FF9800',
      otp: '#9C27B0',
      transactional: '#607D8B',
      promotional: '#795548',
    };
    return colors[category] || '#757575';
  }

  getCategoryGradient(category: string): string {
    const gradients: { [key: string]: string } = {
      offers: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      finance: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
      travel: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
      otp: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
      transactional: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
      // Lighter, softer promotional gradient for consistency with new theme
      promotional: 'linear-gradient(135deg, #FFE7B3 0%, #FFD6EA 100%)',
    };
    return (
      gradients[category] || 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    );
  }

  getCategoryIcon(category: string): string {
    const icons: { [key: string]: string } = {
      offers: '🎁',
      finance: '💰',
      travel: '✈️',
      otp: '🔐',
      transactional: '📦',
      promotional: '📢',
    };
    return icons[category] || '📧';
  }
}
