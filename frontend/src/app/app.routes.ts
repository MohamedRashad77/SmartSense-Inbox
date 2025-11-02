import { Routes } from '@angular/router';
import { Inbox } from './components/inbox/inbox';
import { Summary } from './components/summary/summary';

export const routes: Routes = [
  { path: '', redirectTo: '/inbox', pathMatch: 'full' },
  { path: 'inbox', component: Inbox },
  { path: 'summary', component: Summary },
];
