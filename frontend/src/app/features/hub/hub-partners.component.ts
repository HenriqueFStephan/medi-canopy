import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

import { TranslatePipe } from '../../core/i18n';
import { HUB_PARTNERS, HubPartner } from './hub.data';

@Component({
  selector: 'app-hub-partners',
  standalone: true,
  imports: [CommonModule, TranslatePipe],
  template: `
    <section class="hub-section" aria-labelledby="hub-partners-title">
      <h2 id="hub-partners-title" class="hub-section__title">{{ 'hub.partnersTitle' | t }}</h2>
      <p class="hub-section__intro">{{ 'hub.partnersIntro' | t }}</p>

      <div class="hub-card-grid" *ngIf="partners.length; else emptyState">
        <article class="hub-card" *ngFor="let partner of partners">
          <div class="hub-card__logo-wrap">
            <img
              class="hub-card__logo"
              [src]="partner.logoUrl"
              [alt]="'hub.logoAlt' | t:{ name: partner.name }"
              width="80"
              height="80"
              loading="lazy"
            />
          </div>

          <div class="hub-card__body">
            <p class="hub-card__area">{{ partner.area }}</p>
            <h3 class="hub-card__name">{{ partner.name }}</h3>
            <p class="hub-card__desc">{{ partner.description }}</p>
            <a
              class="hub-card__link"
              [href]="partner.website"
              target="_blank"
              rel="noopener noreferrer"
            >
              {{ 'hub.visitSite' | t }}
            </a>
          </div>
        </article>
      </div>

      <ng-template #emptyState>
        <p class="hub-empty" role="status">{{ 'hub.partnersEmpty' | t }}</p>
      </ng-template>
    </section>
  `,
  styleUrls: ['./hub-cards.scss', './hub-layout.component.scss'],
})
export class HubPartnersComponent {
  readonly partners: HubPartner[] = HUB_PARTNERS;
}
