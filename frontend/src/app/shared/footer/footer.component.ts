import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [RouterLink],
  template: `
    <footer class="footer">
      <div class="container">
        <p>&copy; {{ year }} {{ siteName }} · Informação confiável sobre cannabis</p>
        <p>
          <a routerLink="/news">Notícias</a>
          ·
          <a routerLink="/blog">Blog</a>
          ·
          <a routerLink="/contact">Contato</a>
          ·
          <a [href]="instagramUrl" target="_blank" rel="noopener">Instagram</a>
        </p>
      </div>
    </footer>
  `,
  styleUrls: ['./footer.component.scss'],
})
export class FooterComponent {
  readonly year = new Date().getFullYear();
  readonly siteName = environment.siteName;
  readonly instagramUrl = environment.instagramUrl;
}
