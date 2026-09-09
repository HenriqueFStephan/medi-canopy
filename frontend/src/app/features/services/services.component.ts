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
    <section class="section">
      <div class="container">
        <header class="page-header">
          <h1>Consultoria Técnica e Estratégica em Cannabis Medicinal</h1>
          <p>
            Visão integrada de toda a cadeia produtiva — da concepção e implantação da unidade ao cultivo,
            processamento e operação comercial.
          </p>
        </header>

        <div *ngIf="loading" class="loading">Carregando serviços…</div>
        <div *ngIf="error" class="error-state">{{ error }}</div>

        <ul class="feature-list" *ngIf="!loading && !error">
          <li *ngFor="let svc of services">
            <div>
              <h3>{{ displayTitle(svc.title) }}</h3>
              <p>{{ svc.description }}</p>
              <ul class="highlights" *ngIf="svc.highlights.length">
                <li *ngFor="let h of svc.highlights">{{ h }}</li>
              </ul>
            </div>
          </li>
        </ul>
      </div>
    </section>

    <section class="cta-minimal">
      <div class="container">
        <h2>Pronto para estruturar seu projeto?</h2>
        <p>Agende uma conversa para mapear instalação, climatização, cultivo e compliance.</p>
        <a routerLink="/contact" class="btn btn--primary">Solicitar consultoria</a>
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

  /** CSS already numbers .feature-list rows; drop the same index from API titles. */
  displayTitle(title: string): string {
    return title.replace(/^\s*\d+\s*[—–−-]\s*/, '').trim();
  }

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
