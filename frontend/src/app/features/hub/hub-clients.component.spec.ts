import { ComponentFixture, TestBed } from '@angular/core/testing';
import { I18nService } from '../../core/i18n';
import { HubClientsComponent } from './hub-clients.component';
import { HUB_CLIENTS } from './hub.data';

describe('HubClientsComponent', () => {
  let fixture: ComponentFixture<HubClientsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HubClientsComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(HubClientsComponent);
    TestBed.inject(I18nService).setLang('pt-BR');
    fixture.detectChanges();
  });

  it('shows the clients section title', () => {
    const title = fixture.nativeElement.querySelector('#hub-clients-title');
    expect(title?.textContent?.trim()).toBe('Clientes Medi Canopy');
  });

  it('shows the clients section intro', () => {
    const intro = fixture.nativeElement.querySelector('.hub-section__intro');
    expect(intro?.textContent?.trim()).toBe(
      'Empresas para as quais a Medi Canopy já prestou serviços ou desenvolveu projetos — um histórico de atuação no setor de cannabis medicinal.',
    );
  });

  it('shows PlantManager as a client card with website CTA', () => {
    expect(HUB_CLIENTS.length).toBeGreaterThan(0);

    const plantManager = HUB_CLIENTS.find((c) => c.id === 'plantmanager');
    expect(plantManager).withContext('PlantManager client entry').toBeTruthy();

    const cards = fixture.nativeElement.querySelectorAll('.hub-card');
    expect(cards.length).toBe(HUB_CLIENTS.length);

    const card = cards[0];
    expect(card.classList.contains('hub-card--extended')).toBeTrue();
    expect(card.querySelector('.hub-card__name')?.textContent?.trim()).toBe('PlantManager');
    expect(card.querySelector('.hub-card__area')?.textContent?.trim()).toBe('Tecnologia');
    expect(card.querySelector('.hub-card__desc')?.textContent?.trim()).toBe(plantManager!.description);

    const logo = card.querySelector('.hub-card__logo') as HTMLImageElement;
    expect(logo?.src).toContain('/assets/clients/plantmanager.png');
    expect(logo?.alt).toBe('Logo PlantManager');

    const link = card.querySelector('.hub-card__link') as HTMLAnchorElement;
    expect(link?.href).toBe('https://plantmanager.com.br/');
    expect(link?.target).toBe('_blank');
    expect(link?.rel).toContain('noopener');
    expect(link?.textContent?.trim()).toBe('Conheça a PlantManager →');
  });

  it('shows Medi Canopy and Genesis highlight blocks for PlantManager', () => {
    const card = fixture.nativeElement.querySelector('.hub-card');
    const highlights = card.querySelectorAll('.hub-card__highlight');
    expect(highlights.length).toBe(2);

    const mediCanopyTitle = highlights[0].querySelector('.hub-card__highlight-title');
    expect(mediCanopyTitle?.textContent?.trim()).toBe('Atuação da Medi Canopy');
    expect(mediCanopyTitle?.id).toBe('hub-client-plantmanager-medi-canopy-role');
    expect(highlights[0].querySelector('.hub-card__highlight-desc')?.textContent).toContain('Genesis');

    const genesis = highlights[1];
    expect(genesis.classList.contains('hub-card__highlight--featured')).toBeTrue();
    expect(genesis.querySelector('.hub-card__highlight-title')?.textContent?.trim()).toBe(
      'Genesis — Sistema Operacional de Melhoramento Genético',
    );
    expect(genesis.querySelector('.hub-card__highlight-desc')?.textContent).toContain(
      'melhoramento genético de Cannabis',
    );
  });
});
