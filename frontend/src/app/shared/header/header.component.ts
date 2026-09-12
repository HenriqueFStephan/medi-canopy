import { CommonModule } from '@angular/common';
import { Component, HostListener } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

import { I18nService, Lang, TranslatePipe } from '../../core/i18n';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive, TranslatePipe],
  template: `
    <header class="header">
      <div class="container header__inner">
        <nav class="nav">
          <a routerLink="/services" routerLinkActive="active">{{ 'nav.services' | t }}</a>
          <a routerLink="/blog" routerLinkActive="active">{{ 'nav.blog' | t }}</a>
          <a routerLink="/news" routerLinkActive="active">{{ 'nav.news' | t }}</a>
          <a
            routerLink="/hub"
            routerLinkActive="active"
            [routerLinkActiveOptions]="{ exact: false }"
          >
            {{ 'nav.hub' | t }}
          </a>
          <a routerLink="/courses" routerLinkActive="active">{{ 'nav.courses' | t }}</a>
          <a routerLink="/contact" routerLinkActive="active" class="btn btn--primary nav__cta">
            {{ 'nav.contact' | t }}
          </a>
        </nav>

        <div class="header__brand-cluster">
          <a routerLink="/" class="brand" [attr.aria-label]="'header.homeAria' | t">
            <img
              class="brand__logo"
              src="assets/brand/logo-mark.png"
              alt=""
              width="40"
              height="25"
              decoding="async"
            />
            <span class="brand__name">
              <span class="brand__medi">Medi</span><span class="brand__canopy"> Canopy</span>
            </span>
          </a>

          <div class="lang-dropdown" [class.lang-dropdown--open]="menuOpen">
            <button
              type="button"
              class="lang-dropdown__toggle"
              [attr.aria-label]="'lang.label' | t"
              [attr.aria-expanded]="menuOpen"
              aria-haspopup="listbox"
              (click)="toggleMenu()"
            >
              <span class="lang-dropdown__flag" aria-hidden="true">
                <ng-container *ngIf="i18n.lang() === 'pt-BR'" [ngTemplateOutlet]="flagBr" />
                <ng-container *ngIf="i18n.lang() === 'en'" [ngTemplateOutlet]="flagEn" />
              </span>
              <span class="lang-dropdown__label">{{ currentLabelKey | t }}</span>
              <svg class="lang-dropdown__caret" viewBox="0 0 12 8" aria-hidden="true">
                <path
                  d="M1 1.5L6 6.5L11 1.5"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.6"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </button>

            <ul
              class="lang-dropdown__menu"
              role="listbox"
              [attr.aria-label]="'lang.label' | t"
              *ngIf="menuOpen"
            >
              <li role="none">
                <button
                  type="button"
                  class="lang-dropdown__option"
                  role="option"
                  [attr.aria-selected]="i18n.lang() === 'pt-BR'"
                  [class.lang-dropdown__option--active]="i18n.lang() === 'pt-BR'"
                  (click)="selectLang('pt-BR')"
                >
                  <span class="lang-dropdown__flag" aria-hidden="true">
                    <ng-container [ngTemplateOutlet]="flagBr" />
                  </span>
                  <span>{{ 'lang.pt' | t }}</span>
                </button>
              </li>
              <li role="none">
                <button
                  type="button"
                  class="lang-dropdown__option"
                  role="option"
                  [attr.aria-selected]="i18n.lang() === 'en'"
                  [class.lang-dropdown__option--active]="i18n.lang() === 'en'"
                  (click)="selectLang('en')"
                >
                  <span class="lang-dropdown__flag" aria-hidden="true">
                    <ng-container [ngTemplateOutlet]="flagEn" />
                  </span>
                  <span>{{ 'lang.en' | t }}</span>
                </button>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </header>

    <ng-template #flagBr>
      <svg class="lang-dropdown__flag-svg" viewBox="0 0 28 20" aria-hidden="true">
        <rect width="28" height="20" rx="2" fill="#009b3a" />
        <polygon points="14,2.4 25.2,10 14,17.6 2.8,10" fill="#fedd00" />
        <circle cx="14" cy="10" r="3.6" fill="#002776" />
      </svg>
    </ng-template>
    <ng-template #flagEn>
      <svg class="lang-dropdown__flag-svg" viewBox="0 0 28 20" aria-hidden="true">
        <rect width="28" height="20" rx="2" fill="#b22234" />
        <rect y="1.54" width="28" height="1.54" fill="#fff" />
        <rect y="4.62" width="28" height="1.54" fill="#fff" />
        <rect y="7.69" width="28" height="1.54" fill="#fff" />
        <rect y="10.77" width="28" height="1.54" fill="#fff" />
        <rect y="13.85" width="28" height="1.54" fill="#fff" />
        <rect y="16.92" width="28" height="1.54" fill="#fff" />
        <rect width="12.4" height="10.8" fill="#3c3b6e" />
      </svg>
    </ng-template>
  `,
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent {
  menuOpen = false;

  constructor(readonly i18n: I18nService) {}

  get currentLabelKey(): 'lang.pt' | 'lang.en' {
    return this.i18n.lang() === 'en' ? 'lang.en' : 'lang.pt';
  }

  toggleMenu(): void {
    this.menuOpen = !this.menuOpen;
  }

  selectLang(lang: Lang): void {
    this.i18n.setLang(lang);
    this.menuOpen = false;
  }

  @HostListener('document:click', ['$event'])
  onDocumentClick(event: Event): void {
    const target = event.target as HTMLElement | null;
    if (target?.closest('.lang-dropdown')) {
      return;
    }
    this.menuOpen = false;
  }

  @HostListener('document:keydown.escape')
  onEscape(): void {
    this.menuOpen = false;
  }
}
