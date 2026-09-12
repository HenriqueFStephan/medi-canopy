import { Component, OnDestroy, OnInit } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { Subject, takeUntil } from 'rxjs';

import { ApiService } from '../../core/api.service';
import { I18nService, TranslatePipe } from '../../core/i18n';
import { NewsArticle } from '../../core/models';

@Component({
  selector: 'app-news-list',
  standalone: true,
  imports: [CommonModule, DatePipe, TranslatePipe],
  template: `
    <section class="section">
      <div class="container">
        <header class="page-header">
          <h1>{{ 'news.title' | t }}</h1>
          <p>{{ 'news.lead' | t }}</p>
          <div class="filters">
            <button type="button" class="filter" [class.active]="filter === 'all'" (click)="setFilter('all')">
              {{ 'news.filterAll' | t }}
            </button>
            <button type="button" class="filter" [class.active]="filter === 'BR'" (click)="setFilter('BR')">
              {{ 'news.filterBR' | t }}
            </button>
            <button type="button" class="filter" [class.active]="filter === 'global'" (click)="setFilter('global')">
              {{ 'news.filterGlobal' | t }}
            </button>
          </div>
        </header>

        <div *ngIf="loading" class="loading">{{ 'news.loading' | t }}</div>
        <div *ngIf="error" class="error-state">{{ error | t }}</div>

        <div class="news-rows" *ngIf="!loading && !error">
          <a
            class="news-row"
            *ngFor="let article of articles"
            [href]="article.source_url || '#'"
            [attr.target]="article.source_url ? '_blank' : null"
            rel="noopener"
          >
            <span class="col-date">{{ article.published_at | date:'d MMM y':undefined:i18n.dateLocale() }}</span>
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
export class NewsListComponent implements OnInit, OnDestroy {
  articles: NewsArticle[] = [];
  loading = true;
  error: '' | 'news.error' = '';
  filter: 'all' | 'BR' | 'global' = 'all';
  private readonly destroy$ = new Subject<void>();

  constructor(
    private api: ApiService,
    readonly i18n: I18nService,
  ) {}

  ngOnInit(): void {
    this.load();
    this.i18n.lang$.pipe(takeUntil(this.destroy$)).subscribe(() => this.load());
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
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
        this.error = 'news.error';
        this.loading = false;
      },
    });
  }
}
