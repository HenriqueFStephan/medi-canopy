import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../core/api.service';
import { ServiceOffering } from '../../core/models';

@Component({
  selector: 'app-services',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <section class="hero-services">
      <div class="container">
        <h1>Serviços de consultoria</h1>
        <p>
          Experiência em todo o ciclo do mercado — do projeto do galpão à colheita e operação comercial.
          Referência em projetos como <a href="https://4treesbuilding.ca/projects" target="_blank" rel="noopener">4trees Cannabis Building</a>.
        </p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div *ngIf="loading" class="loading">Carregando serviços…</div>
        <div *ngIf="error" class="error-state">{{ error }}</div>

        <div class="services-grid" *ngIf="!loading && !error">
          <article class="card service-card" *ngFor="let svc of services">
            <div class="service-card__icon" [attr.data-icon]="svc.icon"></div>
            <h2>{{ svc.title }}</h2>
            <p>{{ svc.description }}</p>
            <ul>
              <li *ngFor="let h of svc.highlights">{{ h }}</li>
            </ul>
          </article>
        </div>

        <div class="cta-box">
          <h2>Pronto para estruturar seu projeto?</h2>
          <p>Agende uma conversa para mapear instalação, climatização, cultivo e compliance.</p>
          <a routerLink="/contact" class="btn btn--primary">Solicitar consultoria</a>
        </div>
      </div>
    </section>
  `,
  styleUrls: ['./services.component.scss'],
})
export class ServicesComponent implements OnInit {
  services: ServiceOffering[] = [];
  loading = true;
  error = '';

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.api.getServices().subscribe({
      next: (data) => {
        this.services = data;
        this.loading = false;
      },
      error: () => {
        this.error = 'Não foi possível carregar os serviços.';
        this.loading = false;
      },
    });
  }
}
