import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { I18nService } from '../../core/i18n';
import { FooterComponent } from './footer.component';

describe('FooterComponent', () => {
  let fixture: ComponentFixture<FooterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FooterComponent],
      providers: [provideRouter([])],
    }).compileComponents();

    TestBed.inject(I18nService).setLang('pt-BR');
    fixture = TestBed.createComponent(FooterComponent);
    fixture.detectChanges();
  });

  it('renders the legal company name without a year prefix', () => {
    const legal = fixture.nativeElement.querySelector('.footer__legal');

    expect(legal?.textContent).toContain('Medi Canopy Biotecnologia, Educação e Consultoria Ltda');
    expect(legal?.textContent).not.toMatch(/^\s*2026/);
  });
});
