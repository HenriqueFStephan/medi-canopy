import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [RouterLink],
  template: `
    <footer class="footer">
      <div class="container">
        <p class="footer__legal">{{ legalName }}</p>
        <p>
          <a routerLink="/news">Notícias</a>
          ·
          <a routerLink="/blog">Artigos Científicos</a>
          ·
          <a routerLink="/contact">Contato</a>
        </p>
      </div>
    </footer>
  `,
  styleUrls: ['./footer.component.scss'],
})
export class FooterComponent {
  readonly legalName = '2026 Medi Canopy Biotecnologia, Educação e Consultoria Ltda';
}
