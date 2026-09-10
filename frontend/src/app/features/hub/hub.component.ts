import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HUB_PARTNERS, HubPartner } from './hub.data';

@Component({
  selector: 'app-hub',
  standalone: true,
  imports: [CommonModule],
  template: `
    <section class="section hub-page">
      <div class="container">
        <header class="page-header">
          <h1>Hub</h1>
          <p class="hub-page__lead">
            Parcerias estratégicas com empresas de tecnologia, pesquisa e consultoria
            regulatória, jurídica e de compliance para oferecer soluções integradas ao
            setor de cannabis medicinal.
          </p>
        </header>

        <section class="hub-section" aria-labelledby="hub-partners-title">
          <h2 id="hub-partners-title" class="hub-section__title">Parceiros Medi Canopy</h2>
          <p class="hub-section__intro">
            Conheça as empresas que compõem o ecossistema Medi Canopy — atuando de forma
            integrada em tecnologia, pesquisa, regulação, jurídico e compliance.
          </p>

          <div class="partner-grid" *ngIf="partners.length; else emptyState">
            <article class="partner-card" *ngFor="let partner of partners">
              <div class="partner-card__logo-wrap">
                <img
                  class="partner-card__logo"
                  [src]="partner.logoUrl"
                  [alt]="'Logo ' + partner.name"
                  width="80"
                  height="80"
                  loading="lazy"
                />
              </div>

              <div class="partner-card__body">
                <p class="partner-card__area">{{ partner.area }}</p>
                <h3 class="partner-card__name">{{ partner.name }}</h3>
                <p class="partner-card__desc">{{ partner.description }}</p>
                <a
                  class="partner-card__link"
                  [href]="partner.website"
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
              Estamos ampliando nossa rede de parceiros estratégicos. Em breve, novos
              parceiros serão apresentados aqui.
            </p>
          </ng-template>
        </section>
      </div>
    </section>
  `,
  styleUrls: ['./hub.component.scss'],
})
export class HubComponent {
  readonly partners: HubPartner[] = HUB_PARTNERS;
}
