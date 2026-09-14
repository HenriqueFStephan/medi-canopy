import { Component, OnDestroy, OnInit } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { RouterLink } from '@angular/router';
import { Subject, takeUntil } from 'rxjs';

import { ApiService } from '../../core/api.service';
import { I18nService, TranslatePipe } from '../../core/i18n';
import { NewsArticle } from '../../core/models';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, DatePipe, RouterLink, TranslatePipe],
  template: `
    <section class="hero">
      <div class="container">
        <span class="hero__chip">{{ 'home.chip' | t }}</span>
        <h1>{{ 'home.titleBefore' | t }}<em>{{ 'home.titleEm' | t }}</em>{{ 'home.titleAfter' | t }}</h1>
        <div class="hero__bottom">
          <p class="hero__lead">{{ 'home.lead' | t }}</p>
          <div class="hero__actions">
            <a routerLink="/services" class="btn btn--primary">{{ 'home.ctaStart' | t }}</a>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <h2 class="section__title">{{ 'home.offerTitle' | t }}</h2>
        <div class="feature-list">
          <a routerLink="/services" class="feature-list__item">
            <div>
              <h3>{{ 'home.consultingTitle' | t }}</h3>
              <p>{{ 'home.consultingDesc' | t }}</p>
            </div>
          </a>
          <a routerLink="/courses" class="feature-list__item">
            <div>
              <h3>{{ 'home.coursesTitle' | t }}</h3>
              <p>{{ 'home.coursesDesc' | t }}</p>
            </div>
          </a>
          <a routerLink="/blog" class="feature-list__item">
            <div>
              <h3>{{ 'home.blogTitle' | t }}</h3>
              <p>{{ 'home.blogDesc' | t }}</p>
            </div>
          </a>
        </div>
      </div>
    </section>

    <section class="section news-section" *ngIf="headlines.length">
      <div class="container">
        <h2 class="section__title">{{ 'home.headlinesTitle' | t }}</h2>
        <div class="news-rows">
          <ng-container *ngFor="let article of headlines">
            <a
              *ngIf="article.source_url; else headlineText"
              class="news-row"
              [href]="article.source_url"
              target="_blank"
              rel="noopener"
            >
              <span class="col-date">{{ article.published_at | date:'d MMM y':undefined:i18n.dateLocale() }}</span>
              <span class="col-tag"><span class="tag">{{ article.region }}</span></span>
              <span class="col-title">{{ article.title }}</span>
              <span class="col-arrow">→</span>
            </a>
            <ng-template #headlineText>
              <div class="news-row news-row--static">
                <span class="col-date">{{ article.published_at | date:'d MMM y':undefined:i18n.dateLocale() }}</span>
                <span class="col-tag"><span class="tag">{{ article.region }}</span></span>
                <span class="col-title">{{ article.title }}</span>
              </div>
            </ng-template>
          </ng-container>
        </div>
      </div>
    </section>

    <section class="cta-minimal">
      <div class="container">
        <h2>{{ 'home.ctaTitle' | t }}</h2>
        <p>{{ 'home.ctaLead' | t }}</p>
        <a routerLink="/contact" class="btn btn--primary">{{ 'home.ctaContact' | t }}</a>
      </div>
    </section>
  `,
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit, OnDestroy {
  headlines: NewsArticle[] = [];
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

  private load(): void {
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
