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
          <h1>Artigos Científicos</h1>
          <p>
            Espaço do autor com curadoria humana. Pesquisas científicas e posts do
            <a [href]="instagramUrl" target="_blank" rel="noopener">&#64;papiroebers</a>.
          </p>
        </header>

        <div *ngIf="loading" class="loading">Carregando posts…</div>
        <div *ngIf="error" class="error-state">{{ error }}</div>

        <div class="news-rows" *ngIf="!loading && !error">
          <a class="news-row" *ngFor="let post of posts" [routerLink]="['/blog', post.slug]">
            <span class="col-date">{{ post.published_at | date:'d MMM y' }}</span>
            <span class="col-tag">
              <span class="tag" *ngIf="post.source_type === 'instagram'">Instagram</span>
              <span class="tag" *ngIf="post.source_type === 'agent_research'">Pesquisa</span>
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
        this.error = 'Não foi possível carregar os artigos científicos.';
        this.loading = false;
      },
    });
  }
}
