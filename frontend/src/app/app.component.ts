import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

import { I18nService } from './core/i18n';
import { FooterComponent } from './shared/footer/footer.component';
import { HeaderComponent } from './shared/header/header.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, HeaderComponent, FooterComponent],
  template: `
    <app-header />
    <main>
      <router-outlet />
    </main>
    <app-footer />
  `,
  styles: [`
    main {
      min-height: calc(100vh - 140px);
    }
  `],
})
export class AppComponent {
  constructor(_i18n: I18nService) {
    // Ensure document language/title apply on bootstrap.
  }
}
