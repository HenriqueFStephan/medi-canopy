import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [RouterLink, RouterLinkActive],
  template: `
    <header class="header">
      <div class="container header__inner">
        <nav class="nav">
          <a routerLink="/services" routerLinkActive="active">Serviços</a>
          <a routerLink="/blog" routerLinkActive="active">Blog</a>
          <a routerLink="/news" routerLinkActive="active">Notícias</a>
          <a routerLink="/projects" routerLinkActive="active">Projetos</a>
          <a routerLink="/courses" routerLinkActive="active">Cursos</a>
          <a routerLink="/contact" routerLinkActive="active" class="btn btn--primary nav__cta">Contato</a>
          <a [href]="instagramUrl" target="_blank" rel="noopener" class="nav__ig">Instagram</a>
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
export class HeaderComponent {
  readonly instagramUrl = environment.instagramUrl;
}
