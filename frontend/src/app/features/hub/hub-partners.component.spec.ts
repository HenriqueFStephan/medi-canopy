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

  it('shows the partners section intro', () => {
    const intro = fixture.nativeElement.querySelector('.hub-section__intro');
    expect(intro?.textContent?.trim()).toBe(
      'Conheça as organizações que integram o ecossistema Medi Canopy, reunindo associações de pacientes, empresas e parceiros estratégicos em diferentes frentes da cannabis medicinal.',
    );
  });

  it('shows an empty state when there are no partners', () => {
    expect(HUB_PARTNERS.length).toBe(0);
    const empty = fixture.nativeElement.querySelector('.hub-empty');
    expect(empty).withContext('empty state message').toBeTruthy();
  });
});
