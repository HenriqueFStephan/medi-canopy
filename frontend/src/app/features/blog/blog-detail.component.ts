import { Component, OnDestroy, OnInit } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { Subject, takeUntil } from 'rxjs';

import { ApiService } from '../../core/api.service';
import { I18nService, TranslatePipe } from '../../core/i18n';
import { BlogPost } from '../../core/models';

@Component({
  selector: 'app-blog-detail',
  standalone: true,
  imports: [CommonModule, DatePipe, RouterLink, TranslatePipe],
  template: `
    <section class="section" *ngIf="post">
      <article class="container article">
        <a routerLink="/blog" class="back">{{ 'blog.back' | t }}</a>
        <header>
          <span class="tag" *ngIf="post.source_type === 'agent_research'">{{ 'blog.researchTag' | t }}</span>
          <h1>{{ post.title }}</h1>
          <p class="article__meta">
            {{ post.author_name }} · {{ post.published_at | date:'longDate':undefined:i18n.dateLocale() }}
          </p>
        </header>
        <div class="article__body" [innerHTML]="renderedContent"></div>
      </article>
    </section>
    <div *ngIf="loading" class="loading">{{ 'blog.detailLoading' | t }}</div>
    <div *ngIf="error" class="error-state container">{{ error | t }}</div>
  `,
  styleUrls: ['./blog-detail.component.scss'],
})
export class BlogDetailComponent implements OnInit, OnDestroy {
  post: BlogPost | null = null;
  loading = true;
  error: '' | 'blog.notFound' = '';
  renderedContent = '';
  private readonly destroy$ = new Subject<void>();

  constructor(
    private route: ActivatedRoute,
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
    const slug = this.route.snapshot.paramMap.get('slug');
    if (!slug) {
      this.error = 'blog.notFound';
      this.loading = false;
      return;
    }
    this.loading = true;
    this.error = '';
    this.post = null;
    this.api.getBlogBySlug(slug).subscribe({
      next: (data) => {
        this.post = data;
        this.renderedContent = this.simpleMarkdown(data.content_markdown);
        this.loading = false;
      },
      error: () => {
        this.error = 'blog.notFound';
        this.loading = false;
      },
    });
  }

  /** Minimal markdown → HTML for demo (headings, paragraphs, links). */
  private simpleMarkdown(md: string): string {
    return md
      .replace(/^### (.*$)/gim, '<h3>$1</h3>')
      .replace(/^## (.*$)/gim, '<h2>$1</h2>')
      .replace(/^# (.*$)/gim, '<h1>$1</h1>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
      .replace(/^---$/gim, '<hr>')
      .replace(/\n\n/g, '</p><p>')
      .replace(/^(?!<[h|p|u|a|hr])/gim, (line) => (line.trim() ? `<p>${line}</p>` : ''));
  }
}
