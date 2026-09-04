import { Component, OnInit } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { ApiService } from '../../core/api.service';
import { NewsArticle } from '../../core/models';

@Component({
  selector: 'app-news-list',
  standalone: true,
  imports: [CommonModule, DatePipe],
  template: `
    <section class="section">
      <div class="container">
        <header class="page-header">
          <h1>Notícias</h1>
          <p>Curadoria diária sobre mercado, medicina, política e indústria. Foco Brasil, cobertura global.</p>
          <div class="filters">
            <button type="button" class="filter" [class.active]="filter === 'all'" (click)="setFilter('all')">Todas</button>
            <button type="button" class="filter" [class.active]="filter === 'BR'" (click)="setFilter('BR')">Brasil</button>
            <button type="button" class="filter" [class.active]="filter === 'global'" (click)="setFilter('global')">Global</button>
          </div>
        </header>

        <div *ngIf="loading" class="loading">Carregando notícias…</div>
        <div *ngIf="error" class="error-state">{{ error }}</div>

        <div class="news-rows" *ngIf="!loading && !error">
          <a
            class="news-row"
            *ngFor="let article of articles"
            [href]="article.source_url || '#'"
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
  `,
  styleUrls: ['./news-list.component.scss'],
})
export class NewsListComponent implements OnInit {
  articles: NewsArticle[] = [];
  loading = true;
  error = '';
  filter: 'all' | 'BR' | 'global' = 'all';

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.load();
  }

  setFilter(f: 'all' | 'BR' | 'global'): void {
    this.filter = f;
    this.load();
  }

  private load(): void {
    this.loading = true;
    this.error = '';
    const region = this.filter === 'all' ? undefined : this.filter;
    this.api.getNews(region).subscribe({
      next: (data) => {
        this.articles = data;
        this.loading = false;
      },
      error: () => {
        this.error = 'Não foi possível carregar as notícias. Verifique se o backend está em execução.';
        this.loading = false;
      },
    });
  }
}
