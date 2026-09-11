import { Component, OnInit } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ApiService } from '../../core/api.service';
import { BlogPost } from '../../core/models';

@Component({
  selector: 'app-blog-detail',
  standalone: true,
  imports: [CommonModule, DatePipe, RouterLink],
  template: `
    <section class="section" *ngIf="post">
      <article class="container article">
        <a routerLink="/blog" class="back">← Voltar aos artigos científicos</a>
        <header>
          <span class="tag" *ngIf="post.source_type === 'agent_research'">Pesquisa</span>
          <h1>{{ post.title }}</h1>
          <p class="article__meta">
            {{ post.author_name }} · {{ post.published_at | date:'longDate' }}
          </p>
        </header>
        <div class="article__body" [innerHTML]="renderedContent"></div>
      </article>
    </section>
    <div *ngIf="loading" class="loading">Carregando…</div>
    <div *ngIf="error" class="error-state container">{{ error }}</div>
  `,
  styleUrls: ['./blog-detail.component.scss'],
})
export class BlogDetailComponent implements OnInit {
  post: BlogPost | null = null;
  loading = true;
  error = '';
  renderedContent = '';

  constructor(
    private route: ActivatedRoute,
    private api: ApiService,
  ) {}

  ngOnInit(): void {
    const slug = this.route.snapshot.paramMap.get('slug');
    if (!slug) {
      this.error = 'Post não encontrado.';
      this.loading = false;
      return;
    }
    this.api.getBlogBySlug(slug).subscribe({
      next: (data) => {
        this.post = data;
        this.renderedContent = this.simpleMarkdown(data.content_markdown);
        this.loading = false;
      },
      error: () => {
        this.error = 'Post não encontrado.';
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
