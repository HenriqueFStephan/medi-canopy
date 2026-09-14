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

  it('shows 4Trees Cannabis Building as a client card', () => {
    expect(HUB_CLIENTS.length).toBeGreaterThan(0);

    const fourTrees = HUB_CLIENTS.find((c) => c.id === '4trees-cannabis-building');
    expect(fourTrees).withContext('4Trees client entry').toBeTruthy();

    const cards = fixture.nativeElement.querySelectorAll('.hub-card');
    expect(cards.length).toBe(HUB_CLIENTS.length);

    const card = cards[0];
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
    expect(fourTrees?.mediCanopyInvolvement).toBeTruthy();

    const card = fixture.nativeElement.querySelector('.hub-card');
    const involvement = card.querySelector('.hub-card__involvement');
    expect(involvement).withContext('Medi Canopy involvement block').toBeTruthy();

    expect(card.querySelector('.hub-card__involvement-brand')?.textContent?.trim()).toBe('Medi Canopy');
    expect(card.querySelector('.hub-card__involvement-title')?.textContent?.trim()).toBe(
      'Atuação da Medi Canopy',
    );
    expect(card.querySelector('.hub-card__involvement-role')?.textContent?.trim()).toBe(
      fourTrees!.mediCanopyInvolvement!.role,
    );
    expect(card.querySelector('.hub-card__involvement-desc')?.textContent?.trim()).toBe(
      fourTrees!.mediCanopyInvolvement!.description,
    );
  });
});
