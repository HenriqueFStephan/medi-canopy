import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [RouterLink],
  template: `
    <section class="hero">
      <div class="container hero__content">
        <p class="hero__eyebrow">Hub de informação · Brasil &amp; mundo</p>
        <h1>Informação confiável sobre <em>cannabis</em></h1>
        <p class="hero__lead">
          Notícias curadas, blog com rigor científico, cursos e consultoria completa —
          do projeto do galpão à colheita.
        </p>
        <div class="hero__actions">
          <a routerLink="/news" class="btn btn--primary">Ver notícias</a>
          <a routerLink="/services" class="btn btn--outline">Consultoria</a>
          <a [href]="instagramUrl" target="_blank" rel="noopener" class="btn btn--accent">
            Seguir no Instagram
          </a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <h2 class="section__title">O que você encontra aqui</h2>
        <div class="grid">
          <a routerLink="/news" class="card feature-card">
            <span class="feature-card__num">01</span>
            <h3>Notícias</h3>
            <p>Mercado, política, medicina e indústria — fontes confiáveis, curadoria diária por agente.</p>
          </a>
          <a routerLink="/blog" class="card feature-card">
            <span class="feature-card__num">02</span>
            <h3>Blog</h3>
            <p>Espaço do autor + pesquisas científicas revisadas. Conteúdo do Instagram integrado.</p>
          </a>
          <a routerLink="/courses" class="card feature-card">
            <span class="feature-card__num">03</span>
            <h3>Cursos</h3>
            <p>Formação em cultivo indoor e compliance — arquitetura pronta, lançamento em breve.</p>
          </a>
          <a routerLink="/services" class="card feature-card">
            <span class="feature-card__num">04</span>
            <h3>Serviços</h3>
            <p>Consultoria ponta a ponta: instalação, climatização, cultivo e negócio.</p>
          </a>
        </div>
      </div>
    </section>

    <section class="section section--dark">
      <div class="container cta">
        <h2>Do homegrown ao headquarters</h2>
        <p>Experiência real em todo o ciclo do mercado — inspirado em projetos de referência internacional.</p>
        <a routerLink="/contact" class="btn btn--accent">Fale conosco</a>
      </div>
    </section>
  `,
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent {
  readonly instagramUrl = environment.instagramUrl;
}
