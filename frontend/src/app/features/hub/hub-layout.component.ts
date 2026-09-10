import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-hub-layout',
  standalone: true,
  imports: [RouterLink, RouterLinkActive, RouterOutlet],
  template: `
    <section class="section hub-page">
      <div class="container">
        <header class="page-header">
          <h1>Hub</h1>
          <p class="hub-page__lead">
            Explore o ecossistema Medi Canopy — parceiros estratégicos e empresas
            atendidas em projetos de tecnologia, pesquisa, regulação, jurídico e
            compliance no setor de cannabis medicinal.
          </p>
        </header>

        <nav class="hub-nav" aria-label="Seções do Hub">
          <a
            class="hub-nav__link"
            routerLink="/hub/parceiros"
            routerLinkActive="hub-nav__link--active"
          >
            Parceiros
          </a>
          <a
            class="hub-nav__link"
            routerLink="/hub/clientes"
            routerLinkActive="hub-nav__link--active"
          >
            Clientes
          </a>
        </nav>

        <router-outlet />
      </div>
    </section>
  `,
  styleUrls: ['./hub-layout.component.scss'],
})
export class HubLayoutComponent {}
