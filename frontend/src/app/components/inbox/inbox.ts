import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SmsService } from '../../services/sms.service';
import { Sms } from '../../models/sms.model';

@Component({
  selector: 'app-inbox',
  imports: [CommonModule, FormsModule],
  templateUrl: './inbox.html',
  styleUrl: './inbox.css',
})
export class Inbox implements OnInit {
  smsMessages: Sms[] = [];
  filteredMessages: Sms[] = [];
  loading: boolean = true;
  searchText: string = '';

  // Filters
  selectedCategory: string = '';
  selectedDate: string = '';
  showThreatsOnly: boolean = false;

  // Available categories
  categories: string[] = [
    'offers',
    'finance',
    'travel',
    'otp',
    'transactional',
    'promotional',
  ];

  constructor(private smsService: SmsService) {}

  ngOnInit(): void {
    this.loadMessages();
  }

  loadMessages(): void {
    this.loading = true;
    this.smsService
      .getMessages(
        this.selectedDate,
        this.selectedCategory,
        this.showThreatsOnly
      )
      .subscribe({
        next: (messages: Sms[]) => {
          this.smsMessages = messages;
          this.applySearchFilter();
          this.loading = false;
        },
        error: (error) => {
          console.error('Error loading SMS messages', error);
          this.loading = false;
        },
      });
  }

  applySearchFilter(): void {
    if (!this.searchText.trim()) {
      this.filteredMessages = this.smsMessages;
      return;
    }

    const search = this.searchText.toLowerCase();
    this.filteredMessages = this.smsMessages.filter(
      (msg) =>
        msg.sender.toLowerCase().includes(search) ||
        msg.body.toLowerCase().includes(search) ||
        (msg.category && msg.category.toLowerCase().includes(search))
    );
  }

  applyFilters(): void {
    if (this.searchText.trim()) {
      this.applySearchFilter();
    } else {
      this.loadMessages();
    }
  }

  clearFilters(): void {
    this.selectedCategory = '';
    this.selectedDate = '';
    this.showThreatsOnly = false;
    this.searchText = '';
    this.loadMessages();
  }

  toggleThreats(): void {
    this.showThreatsOnly = !this.showThreatsOnly;
    this.applyFilters();
  }

  hasActiveFilters(): boolean {
    return !!(
      this.selectedCategory ||
      this.selectedDate ||
      this.showThreatsOnly ||
      this.searchText
    );
  }

  getThreatCount(): number {
    return this.filteredMessages.filter((m) => m.is_threat).length;
  }

  getUnreadCount(): number {
    const uniqueCategories = new Set(
      this.filteredMessages.map((m) => m.category)
    );
    return uniqueCategories.size;
  }

  hasAnyTag(sms: Sms): boolean {
    return !!(
      sms.has_otp ||
      sms.has_money_request ||
      (sms.urls && sms.urls.length > 0)
    );
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
      // Lighter, softer promotional gradient to match the new clean theme
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

  getAvatarColor(sender: string): string {
    const colors = [
      'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
      'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
      'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
      'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    ];
    const hash = sender
      .split('')
      .reduce((acc, char) => acc + char.charCodeAt(0), 0);
    return colors[hash % colors.length];
  }

  getInitial(sender: string): string {
    return sender.charAt(0).toUpperCase();
  }

  formatTime(timestamp: Date | string): string {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;

    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  }

  highlightSearch(text: string): string {
    if (!this.searchText.trim()) return text;

    const regex = new RegExp(`(${this.searchText})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
  }

  getThreatClass(message: Sms): string {
    return message.is_threat ? 'threat-message' : '';
  }
}
