import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

import { TranslatePipe } from '../../core/i18n';

@Component({
  selector: 'app-hub-layout',
  standalone: true,
  imports: [RouterLink, RouterLinkActive, RouterOutlet, TranslatePipe],
  template: `
    <section class="section hub-page">
      <div class="container">
        <header class="page-header">
          <h1>{{ 'hub.title' | t }}</h1>
          <p class="hub-page__lead">{{ 'hub.lead' | t }}</p>
        </header>

        <nav class="hub-nav" [attr.aria-label]="'hub.navAria' | t">
          <a
            class="hub-nav__link"
            routerLink="/hub/parceiros"
            routerLinkActive="hub-nav__link--active"
          >
            {{ 'hub.partners' | t }}
          </a>
          <a
            class="hub-nav__link"
            routerLink="/hub/clientes"
            routerLinkActive="hub-nav__link--active"
          >
            {{ 'hub.clients' | t }}
          </a>
        </nav>

        <router-outlet />
      </div>
    </section>
  `,
  styleUrls: ['./hub-layout.component.scss'],
})
export class HubLayoutComponent {}
