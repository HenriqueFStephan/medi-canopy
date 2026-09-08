import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  CANNABIS_PROJECTS,
  CannabisProject,
  categoryLabel,
} from './projects.data';

@Component({
  selector: 'app-projects',
  standalone: true,
  imports: [CommonModule],
  template: `
    <section class="section projects-page">
      <div class="container">
        <header class="page-header">
          <h1>Projetos</h1>
          <p>
            Iniciativas públicas brasileiras sobre cannabis medicinal, industrial e agrícola —
            associações, universidades e centros de pesquisa que avançam o setor no país.
          </p>
        </header>

        <div class="project-cards">
          <article
            class="project-card"
            *ngFor="let project of projects"
            [style.--project-bg]="project.theme.bg"
            [style.--project-surface]="project.theme.surface"
            [style.--project-accent]="project.theme.accent"
            [style.--project-text]="project.theme.text"
            [style.--project-muted]="project.theme.muted"
            [style.--project-border]="project.theme.border"
            [style.--project-tag-bg]="project.theme.tagBg"
            [style.--project-tag-text]="project.theme.tagText"
            [style.--project-font-heading]="project.theme.fontHeading"
          >
            <div class="project-card__banner">
              <span class="project-card__badge">{{ project.shortName }}</span>
              <span class="project-card__location">{{ project.location }}</span>
            </div>

            <div class="project-card__body">
              <div class="project-card__intro">
                <h2>{{ project.name }}</h2>
                <p class="project-card__org">{{ project.organization }}</p>
                <p class="project-card__desc">{{ project.description }}</p>
              </div>

              <ul class="project-card__highlights">
                <li *ngFor="let item of project.highlights">{{ item }}</li>
              </ul>

              <div class="project-card__footer">
                <div class="project-card__tags">
                  <span class="project-card__tag" *ngFor="let cat of project.categories">
                    {{ labelCategory(cat) }}
                  </span>
                </div>
                <a
                  class="project-card__link"
                  [href]="project.website"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Visitar site oficial →
                </a>
              </div>
            </div>
          </article>
        </div>
      </div>
    </section>
  `,
  styleUrls: ['./projects.component.scss'],
})
export class ProjectsComponent {
  readonly projects: CannabisProject[] = CANNABIS_PROJECTS;

  labelCategory = categoryLabel;
}
