import { Component, OnDestroy, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Subject, takeUntil } from 'rxjs';

import { ApiService } from '../../core/api.service';
import { I18nService, TranslatePipe } from '../../core/i18n';
import { Course } from '../../core/models';

@Component({
  selector: 'app-courses',
  standalone: true,
  imports: [CommonModule, TranslatePipe],
  template: `
    <section class="section">
      <div class="container">
        <header class="page-header">
          <h1>{{ 'courses.title' | t }}</h1>
          <p>{{ 'courses.lead' | t }}</p>
        </header>

        <div *ngIf="loading" class="loading">{{ 'courses.loading' | t }}</div>
        <div *ngIf="error" class="error-state">{{ error | t }}</div>

        <div class="feature-list" *ngIf="!loading && !error">
          <article class="feature-list__item course-row" *ngFor="let course of courses">
            <div>
              <span class="tag" *ngIf="course.coming_soon">{{ 'courses.comingSoon' | t }}</span>
              <h3>{{ course.title }}</h3>
              <p class="course-row__level">{{ course.level }}</p>
              <p>{{ course.description }}</p>
              <p class="course-row__price" *ngIf="course.price_display">{{ course.price_display }}</p>
              <ul class="modules" *ngIf="course.modules.length">
                <li *ngFor="let m of course.modules">
                  <strong>{{ m.title }}</strong> — {{ 'courses.moduleDuration' | t:{ minutes: m.duration_minutes } }}
                </li>
              </ul>
              <button type="button" class="btn btn--outline" disabled>
                {{ 'courses.enrollSoon' | t }}
              </button>
            </div>
          </article>
        </div>
      </div>
    </section>
  `,
  styleUrls: ['./courses.component.scss'],
})
export class CoursesComponent implements OnInit, OnDestroy {
  courses: Course[] = [];
  loading = true;
  error: '' | 'courses.error' = '';
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
    this.api.getCourses().subscribe({
      next: (data) => {
        this.courses = data;
        this.loading = false;
      },
      error: () => {
        this.error = 'courses.error';
        this.loading = false;
      },
    });
  }
}
