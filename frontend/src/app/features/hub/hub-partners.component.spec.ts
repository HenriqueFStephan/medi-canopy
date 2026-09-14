import { ComponentFixture, TestBed } from '@angular/core/testing';
import { I18nService } from '../../core/i18n';
import { HubPartnersComponent } from './hub-partners.component';
import { HUB_PARTNERS, HubPartner } from './hub.data';

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

  function partnerCard(partnerId: string): Element {
    const index = HUB_PARTNERS.findIndex((p) => p.id === partnerId);
    return fixture.nativeElement.querySelectorAll('.hub-card')[index];
  }

  function expectPartnerCard(partner: HubPartner, expectedLinkLabel: string): void {
    const card = partnerCard(partner.id);
    expect(card).withContext(`${partner.id} partner card`).toBeTruthy();

    expect(card.querySelector('.hub-card__name')?.textContent?.trim()).toBe(partner.name);
    expect(card.querySelector('.hub-card__area')?.textContent?.trim()).toBe(partner.area);
    expect(card.querySelector('.hub-card__desc')?.textContent?.trim()).toBe(partner.description);

    const logo = card.querySelector('.hub-card__logo') as HTMLImageElement;
    expect(logo?.src).toContain(partner.logoUrl);
    expect(logo?.alt).toBe(`Logo ${partner.name}`);

    const link = card.querySelector('.hub-card__link') as HTMLAnchorElement;
    expect(link?.href).toBe(partner.website);
    expect(link?.textContent?.trim()).toBe(expectedLinkLabel);
    expect(link?.target).toBe('_blank');
    expect(link?.rel).toContain('noopener');
  }

  it('shows the partners section title', () => {
    const title = fixture.nativeElement.querySelector('#hub-partners-title');
    expect(title?.textContent?.trim()).toBe('Parceiros Medi Canopy');
  });

  it('renders one card per partner', () => {
    expect(HUB_PARTNERS.length).toBeGreaterThan(0);

    const cards = fixture.nativeElement.querySelectorAll('.hub-card');
    expect(cards.length).toBe(HUB_PARTNERS.length);
  });

  it('shows Green Growth as a partner card', () => {
    const greenGrowth = HUB_PARTNERS.find((p) => p.id === 'green-growth');
    expect(greenGrowth).withContext('Green Growth partner entry').toBeTruthy();
    expectPartnerCard(greenGrowth!, 'Visitar site →');
  });

  it('shows OM as a partner card with Instagram CTA', () => {
    const om = HUB_PARTNERS.find((p) => p.id === 'associacao-om');
    expect(om).withContext('OM partner entry').toBeTruthy();
    expectPartnerCard(om!, 'Visite o Instagram →');
  });
});
