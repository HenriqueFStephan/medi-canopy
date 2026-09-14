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

  it('shows 4Trees Cannabis Building as a client card', () => {
    const fourTrees = HUB_CLIENTS.find((c) => c.id === '4trees-cannabis-building');
    expect(fourTrees).withContext('4Trees client entry').toBeTruthy();

    const cards = fixture.nativeElement.querySelectorAll('.hub-card');
    const card = cards[1];
    expect(card.classList.contains('hub-card--extended')).toBeTrue();
    expect(card.querySelector('.hub-card__name')?.textContent?.trim()).toBe('4Trees Cannabis Building');
    expect(card.querySelector('.hub-card__area')?.textContent?.trim()).toBe('Consultoria e Operações');
    expect(card.querySelector('.hub-card__desc')?.textContent?.trim()).toBe(fourTrees!.description);

    const logo = card.querySelector('.hub-card__logo') as HTMLImageElement;
    expect(logo?.src).toContain('/assets/clients/4trees-cannabis-building.webp');
    expect(logo?.alt).toBe('Logo 4Trees Cannabis Building');

    const link = card.querySelector('.hub-card__link') as HTMLAnchorElement;
    expect(link?.href).toBe('https://4treesbuilding.ca/projects');
    expect(link?.target).toBe('_blank');
    expect(link?.rel).toContain('noopener');
    expect(link?.textContent?.trim()).toBe('Conheça os projetos da 4Trees →');
  });

  it('shows Medi Canopy involvement for 4Trees', () => {
    const fourTrees = HUB_CLIENTS.find((c) => c.id === '4trees-cannabis-building');
    const highlight = fourTrees!.highlights![0];

    const cards = fixture.nativeElement.querySelectorAll('.hub-card');
    const card = cards[1];
    const involvement = card.querySelector('.hub-card__highlight');
    expect(involvement).withContext('Medi Canopy involvement block').toBeTruthy();

    expect(card.querySelector('.hub-card__highlight-brand')?.textContent?.trim()).toBe('Medi Canopy');
    expect(card.querySelector('.hub-card__highlight-title')?.textContent?.trim()).toBe(
      'Atuação da Medi Canopy',
    );
    expect(card.querySelector('.hub-card__highlight-role')?.textContent?.trim()).toBe(highlight.role);
    expect(card.querySelector('.hub-card__highlight-desc')?.textContent?.trim()).toBe(
      highlight.description,
    );
  });
});
