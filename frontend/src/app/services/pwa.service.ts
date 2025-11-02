import { Injectable, inject } from '@angular/core';
import {
  SwUpdate,
  VersionReadyEvent,
  UnrecoverableStateEvent,
} from '@angular/service-worker';

@Injectable({ providedIn: 'root' })
export class PwaService {
  private readonly swUpdate = inject(SwUpdate);

  constructor() {
    if (!this.swUpdate.isEnabled) {
      return;
    }

    // Prompt user when a new version is ready
    this.swUpdate.versionUpdates.subscribe((evt) => {
      if ((evt as VersionReadyEvent).type === 'VERSION_READY') {
        const accept = confirm('A new version is available. Reload now?');
        if (accept) {
          // Activate and reload
          this.swUpdate.activateUpdate().then(() => document.location.reload());
        }
      }
    });

    // Handle fatal SW errors
    this.swUpdate.unrecoverable.subscribe((event: UnrecoverableStateEvent) => {
      console.error('Unrecoverable service worker state:', event.reason);
      alert('The app encountered an error and needs to reload. Reloading…');
      document.location.reload();
    });

    // Optional: periodic update checks
    const SIX_HOURS = 6 * 60 * 60 * 1000;
    setInterval(() => {
      this.swUpdate.checkForUpdate().catch(() => {});
    }, SIX_HOURS);
  }
}
