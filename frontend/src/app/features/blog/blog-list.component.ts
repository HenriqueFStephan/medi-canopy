import { Component, OnDestroy, OnInit } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { RouterLink } from '@angular/router';
import { Subject, takeUntil } from 'rxjs';

import { ApiService } from '../../core/api.service';
import { I18nService, TranslatePipe } from '../../core/i18n';
import { BlogPost } from '../../core/models';

@Component({
  selector: 'app-blog-list',
  standalone: true,
  imports: [CommonModule, DatePipe, RouterLink, TranslatePipe],
  template: `
    <section class="section">
      <div class="container">
        <header class="page-header">
          <h1>{{ 'blog.title' | t }}</h1>
          <p>{{ 'blog.lead' | t }}</p>
        </header>

        <div *ngIf="loading" class="loading">{{ 'blog.loading' | t }}</div>
        <div *ngIf="error" class="error-state">{{ error | t }}</div>

        <div class="news-rows" *ngIf="!loading && !error">
          <a class="news-row" *ngFor="let post of posts" [routerLink]="['/blog', post.slug]">
            <span class="col-date">{{ post.published_at | date:'d MMM y':undefined:i18n.dateLocale() }}</span>
            <span class="col-tag">
              <span class="tag" *ngIf="post.source_type === 'agent_research'">{{ 'blog.researchTag' | t }}</span>
            </span>
            <span class="col-title">{{ post.title }}</span>
            <span class="col-arrow">→</span>
          </a>
        </div>
      </div>
    </section>
  `,
  styleUrls: ['./blog-list.component.scss'],
})
export class BlogListComponent implements OnInit, OnDestroy {
  posts: BlogPost[] = [];
  loading = true;
  error: '' | 'blog.error' = '';
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
    this.loading = true;
    this.error = '';
    this.api.getBlogPosts().subscribe({
      next: (data) => {
        this.posts = data;
        this.loading = false;
      },
      error: () => {
        this.error = 'blog.error';
        this.loading = false;
      },
    });
  }
}
