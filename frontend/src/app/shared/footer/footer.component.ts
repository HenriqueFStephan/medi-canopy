import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [RouterLink],
  template: `
    <footer class="footer">
      <div class="container footer__grid">
        <div>
          <p class="footer__brand">
            <span class="logo__cana">Cana</span><span class="logo__hub">Hub</span>
          </p>
          <p class="footer__tagline">Informação confiável sobre cannabis — do campo à política.</p>
        </div>
        <div>
          <h4>Navegação</h4>
          <ul>
            <li><a routerLink="/news">Notícias</a></li>
            <li><a routerLink="/blog">Blog</a></li>
            <li><a routerLink="/courses">Cursos</a></li>
            <li><a routerLink="/services">Serviços</a></li>
            <li><a routerLink="/contact">Contato</a></li>
          </ul>
        </div>
        <div>
          <h4>Autor</h4>
          <p>
            <a [href]="instagramUrl" target="_blank" rel="noopener">&#64;papiroebers</a>
          </p>
          <p class="footer__muted">Consultoria ponta a ponta no ciclo do mercado de cannabis.</p>
        </div>
      </div>
      <div class="footer__bottom container">
        <p>&copy; {{ year }} CanaHub. Todos os direitos reservados.</p>
      </div>
    </footer>
  `,
  styleUrls: ['./footer.component.scss'],
})
export class FooterComponent {
  readonly year = new Date().getFullYear();
  readonly instagramUrl = environment.instagramUrl;
}
