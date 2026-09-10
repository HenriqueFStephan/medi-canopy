import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [RouterLink, RouterLinkActive],
  template: `
    <header class="header">
      <div class="container header__inner">
        <nav class="nav">
          <a routerLink="/services" routerLinkActive="active">Serviços</a>
          <a routerLink="/blog" routerLinkActive="active">Artigos Científicos</a>
          <a routerLink="/news" routerLinkActive="active">Notícias</a>
          <a routerLink="/hub" routerLinkActive="active">Hub</a>
          <a routerLink="/courses" routerLinkActive="active">Cursos</a>
          <a routerLink="/contact" routerLinkActive="active" class="btn btn--primary nav__cta">Contato</a>
        </nav>
        <a routerLink="/" class="brand" aria-label="Medi Canopy — início">
          <img
            class="brand__logo"
            src="assets/brand/logo-mark.png"
            alt=""
            width="40"
            height="25"
            decoding="async"
          />
          <span class="brand__name">
            <span class="brand__medi">Medi</span><span class="brand__canopy"> Canopy</span>
          </span>
        </a>
      </div>
    </header>
  `,
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent {}
