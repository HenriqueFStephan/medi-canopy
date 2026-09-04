import { Component, OnInit } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../core/api.service';
import { NewsArticle } from '../../core/models';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, DatePipe, RouterLink],
  template: `
    <section class="hero">
      <div class="container">
        <span class="hero__chip">Hub de informação · Brasil &amp; mundo</span>
        <h1>Informação que <em>importa</em> para o seu cultivo</h1>
        <div class="hero__bottom">
          <p class="hero__lead">
            Notícias curadas, blog com rigor científico, cursos e consultoria completa —
            do projeto do galpão à colheita.
          </p>
          <div class="hero__actions">
            <a routerLink="/services" class="btn btn--primary">Começar</a>
            <a routerLink="/news" class="btn btn--outline">Notícias</a>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <h2 class="section__title">O que oferecemos</h2>
        <div class="feature-list">
          <a routerLink="/news" class="feature-list__item">
            <div>
              <h3>Notícias</h3>
              <p>Mercado, política, medicina e indústria — fontes confiáveis, curadoria diária.</p>
            </div>
          </a>
          <a routerLink="/blog" class="feature-list__item">
            <div>
              <h3>Blog</h3>
              <p>Espaço do autor e pesquisas científicas revisadas. Conteúdo do Instagram integrado.</p>
            </div>
          </a>
          <a routerLink="/courses" class="feature-list__item">
            <div>
              <h3>Cursos e formação</h3>
              <p>Formação em cultivo indoor e compliance — arquitetura pronta, lançamento em breve.</p>
            </div>
          </a>
          <a routerLink="/services" class="feature-list__item">
            <div>
              <h3>Consultoria</h3>
              <p>Ponta a ponta: instalação, climatização, cultivo e negócio.</p>
            </div>
          </a>
        </div>
      </div>
    </section>

    <section class="section news-section" *ngIf="headlines.length">
      <div class="container">
        <h2 class="section__title">Últimas notícias</h2>
        <div class="news-rows">
          <a
            class="news-row"
            *ngFor="let article of headlines"
            [href]="article.source_url || '/news'"
            [attr.target]="article.source_url ? '_blank' : null"
            rel="noopener"
          >
            <span class="col-date">{{ article.published_at | date:'d MMM y' }}</span>
            <span class="col-tag"><span class="tag">{{ article.region }}</span></span>
            <span class="col-title">{{ article.title }}</span>
            <span class="col-arrow">→</span>
          </a>
        </div>
      </div>
    </section>

    <section class="cta-minimal">
      <div class="container">
        <h2>Pronto para começar?</h2>
        <p>Do homegrown ao headquarters — experiência real em todo o ciclo do mercado.</p>
        <a routerLink="/contact" class="btn btn--primary">Fale conosco</a>
        <span class="cta-minimal__or">ou</span>
        <a [href]="instagramUrl" target="_blank" rel="noopener" class="btn btn--outline">Seguir no Instagram</a>
      </div>
    </section>
  `,
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {
  readonly instagramUrl = environment.instagramUrl;
  headlines: NewsArticle[] = [];

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.api.getNews().subscribe({
      next: (data) => {
        this.headlines = data.slice(0, 5);
      },
      error: () => {
        this.headlines = [];
      },
    });
  }
}
