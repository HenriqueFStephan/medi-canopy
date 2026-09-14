import { ComponentFixture, TestBed } from '@angular/core/testing';
import { I18nService } from '../../core/i18n';
import { HubPartnersComponent } from './hub-partners.component';
import { HUB_PARTNERS } from './hub.data';

describe('HubPartnersComponent', () => {
  let fixture: ComponentFixture<HubPartnersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HubPartnersComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(HubPartnersComponent);
    TestBed.inject(I18nService).setLang('pt-BR');
    fixture.detectChanges();
  });

  it('shows the partners section title', () => {
    const title = fixture.nativeElement.querySelector('#hub-partners-title');
    expect(title?.textContent?.trim()).toBe('Parceiros Medi Canopy');
  });

  it('shows Green Growth as a partner card', () => {
    expect(HUB_PARTNERS.length).toBeGreaterThan(0);

    const cards = fixture.nativeElement.querySelectorAll('.hub-card');
    expect(cards.length).toBe(HUB_PARTNERS.length);

    const greenGrowth = HUB_PARTNERS.find((p) => p.id === 'green-growth');
    expect(greenGrowth).withContext('Green Growth partner entry').toBeTruthy();

    const card = cards[0];
    expect(card.querySelector('.hub-card__name')?.textContent?.trim()).toBe('Green Growth');
    expect(card.querySelector('.hub-card__area')?.textContent?.trim()).toBe('Jurídico e Regulatório');
    expect(card.querySelector('.hub-card__desc')?.textContent?.trim()).toBe(greenGrowth!.description);

    const logo = card.querySelector('.hub-card__logo') as HTMLImageElement;
    expect(logo?.src).toContain('/assets/partners/green-growth.png');
    expect(logo?.alt).toBe('Logo Green Growth');

    const link = card.querySelector('.hub-card__link') as HTMLAnchorElement;
    expect(link?.href).toBe('https://greengrowth.group/');
    expect(link?.target).toBe('_blank');
    expect(link?.rel).toContain('noopener');
    expect(link?.textContent?.trim()).toBe('Visitar site →');
  });

  it('shows OM as a partner card with Instagram CTA', () => {
    const om = HUB_PARTNERS.find((p) => p.id === 'om-associacao');
    expect(om).withContext('OM partner entry').toBeTruthy();

    const cards = fixture.nativeElement.querySelectorAll('.hub-card');
    const card = cards[1];
    expect(card.querySelector('.hub-card__name')?.textContent?.trim()).toBe(
      'OM – Associação Multidisciplinar em Práticas Integrativas',
    );
    expect(card.querySelector('.hub-card__area')?.textContent?.trim()).toBe('Práticas Integrativas');
    expect(card.querySelector('.hub-card__desc')?.textContent?.trim()).toBe(
      'Cuidado especializado Humano e Animal. Informação e acesso ao tratamento.',
    );

    const logo = card.querySelector('.hub-card__logo') as HTMLImageElement;
    expect(logo?.src).toContain('/assets/partners/om-associacao.png');
    expect(logo?.alt).toBe('Logo OM – Associação Multidisciplinar em Práticas Integrativas');

    const link = card.querySelector('.hub-card__link') as HTMLAnchorElement;
    expect(link?.href).toBe('https://www.instagram.com/associacaoom/');
    expect(link?.target).toBe('_blank');
    expect(link?.rel).toContain('noopener');
    expect(link?.textContent?.trim()).toBe('Visite o Instagram');
  });
});
