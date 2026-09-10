import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HUB_CLIENTS, HubClient } from './hub.data';

@Component({
  selector: 'app-hub-clients',
  standalone: true,
  imports: [CommonModule],
  template: `
    <section class="hub-section" aria-labelledby="hub-clients-title">
      <h2 id="hub-clients-title" class="hub-section__title">Clientes Medi Canopy</h2>
      <p class="hub-section__intro">
        Empresas para as quais a Medi Canopy já prestou serviços ou desenvolveu
        projetos — um histórico de atuação no setor de cannabis medicinal.
      </p>

      <div class="hub-card-grid" *ngIf="clients.length; else emptyState">
        <article class="hub-card" *ngFor="let client of clients">
          <div class="hub-card__logo-wrap">
            <img
              class="hub-card__logo"
              [src]="client.logoUrl"
              [alt]="'Logo ' + client.name"
              width="80"
              height="80"
              loading="lazy"
            />
          </div>

          <div class="hub-card__body">
            <p class="hub-card__area" *ngIf="client.area">{{ client.area }}</p>
            <h3 class="hub-card__name">{{ client.name }}</h3>
            <p class="hub-card__desc">{{ client.description }}</p>
            <a
              class="hub-card__link"
              [href]="client.website"
              target="_blank"
              rel="noopener noreferrer"
            >
              Visitar site →
            </a>
          </div>
        </article>
      </div>

      <ng-template #emptyState>
        <p class="hub-empty" role="status">
          Estamos organizando nosso portfólio de clientes. Em breve, novas empresas
          atendidas serão apresentadas aqui.
        </p>
      </ng-template>
    </section>
  `,
  styleUrls: ['./hub-cards.scss', './hub-layout.component.scss'],
})
export class HubClientsComponent {
  readonly clients: HubClient[] = HUB_CLIENTS;
}
