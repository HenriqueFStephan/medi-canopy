import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../core/api.service';
import { Course } from '../../core/models';

@Component({
  selector: 'app-courses',
  standalone: true,
  imports: [CommonModule],
  template: `
    <section class="section">
      <div class="container">
        <header class="page-header">
          <h1>Cursos</h1>
          <p>Formação prática em cultivo profissional e compliance — em desenvolvimento.</p>
        </header>

        <div *ngIf="loading" class="loading">Carregando cursos…</div>
        <div *ngIf="error" class="error-state">{{ error }}</div>

        <div class="courses-grid" *ngIf="!loading && !error">
          <article class="card course-card" *ngFor="let course of courses">
            <span class="badge" *ngIf="course.coming_soon">Em breve</span>
            <h2>{{ course.title }}</h2>
            <p class="course-card__level">{{ course.level }}</p>
            <p>{{ course.description }}</p>
            <p class="course-card__price">{{ course.price_display }}</p>
            <div class="modules" *ngIf="course.modules.length">
              <h3>Módulos</h3>
              <ul>
                <li *ngFor="let m of course.modules">
                  <strong>{{ m.title }}</strong> — {{ m.duration_minutes }} min
                  <span class="module-desc">{{ m.description }}</span>
                </li>
              </ul>
            </div>
            <button type="button" class="btn btn--outline" disabled>
              Inscrições em breve
            </button>
          </article>
        </div>
      </div>
    </section>
  `,
  styleUrls: ['./courses.component.scss'],
})
export class CoursesComponent implements OnInit {
  courses: Course[] = [];
  loading = true;
  error = '';

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.api.getCourses().subscribe({
      next: (data) => {
        this.courses = data;
        this.loading = false;
      },
      error: () => {
        this.error = 'Não foi possível carregar os cursos.';
        this.loading = false;
      },
    });
  }
}
