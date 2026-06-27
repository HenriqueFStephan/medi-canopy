import { Component, OnInit } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../core/api.service';
import { BlogPost } from '../../core/models';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-blog-list',
  standalone: true,
  imports: [CommonModule, DatePipe, RouterLink],
  template: `
    <section class="section">
      <div class="container">
        <header class="page-header">
          <h1>Blog</h1>
          <p>
            Espaço do autor com curadoria humana. Pesquisas científicas e posts do
            <a [href]="instagramUrl" target="_blank" rel="noopener">&#64;papiroebers</a>.
          </p>
        </header>

        <div *ngIf="loading" class="loading">Carregando posts…</div>
        <div *ngIf="error" class="error-state">{{ error }}</div>

        <div class="blog-grid" *ngIf="!loading && !error">
          <article class="card blog-card" *ngFor="let post of posts">
            <span class="tag" *ngIf="post.source_type === 'instagram'">Instagram</span>
            <span class="tag" *ngIf="post.source_type === 'agent_research'">Pesquisa</span>
            <h2>
              <a [routerLink]="['/blog', post.slug]">{{ post.title }}</a>
            </h2>
            <p>{{ post.excerpt }}</p>
            <div class="blog-card__meta">
              <span>{{ post.author_name }}</span>
              <span>{{ post.published_at | date:'mediumDate' }}</span>
            </div>
            <a [routerLink]="['/blog', post.slug]" class="read-more">Ler mais →</a>
          </article>
        </div>
      </div>
    </section>
  `,
  styleUrls: ['./blog-list.component.scss'],
})
export class BlogListComponent implements OnInit {
  posts: BlogPost[] = [];
  loading = true;
  error = '';
  readonly instagramUrl = environment.instagramUrl;

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.api.getBlogPosts().subscribe({
      next: (data) => {
        this.posts = data;
        this.loading = false;
      },
      error: () => {
        this.error = 'Não foi possível carregar o blog.';
        this.loading = false;
      },
    });
  }
}
