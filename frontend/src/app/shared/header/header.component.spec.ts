import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { I18nService } from '../../core/i18n';
import { HeaderComponent } from './header.component';

describe('HeaderComponent', () => {
  let fixture: ComponentFixture<HeaderComponent>;
  let i18n: I18nService;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HeaderComponent],
      providers: [provideRouter([])],
    }).compileComponents();

    i18n = TestBed.inject(I18nService);
    i18n.setLang('pt-BR');
    fixture = TestBed.createComponent(HeaderComponent);
    fixture.detectChanges();
  });

  afterEach(() => {
    i18n.setLang('pt-BR');
  });

  it('renders the company logo mark to the left of the company name in the header', () => {
    const brand = fixture.nativeElement.querySelector('.brand');
    const logo = brand?.querySelector('.brand__logo');
    const name = brand?.querySelector('.brand__name');

    expect(brand).withContext('brand link in header').toBeTruthy();
    expect(logo?.getAttribute('src')).toBe('assets/brand/logo-mark.png');
    expect(name?.textContent).toContain('Medi');
    expect(name?.textContent).toContain('Canopy');
    expect(logo?.compareDocumentPosition(name!) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
  });

  it('places the language dropdown to the right of the logo cluster', () => {
    const cluster = fixture.nativeElement.querySelector('.header__brand-cluster');
    const brand = cluster?.querySelector('.brand');
    const dropdown = cluster?.querySelector('.lang-dropdown');

    expect(cluster).toBeTruthy();
    expect(dropdown).toBeTruthy();
    expect(
      brand?.compareDocumentPosition(dropdown!) & Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
    expect(fixture.nativeElement.querySelector('.nav .lang-dropdown')).toBeNull();
  });

  it('switches navigation labels from the language dropdown', () => {
    const nav = fixture.nativeElement.querySelector('.nav') as HTMLElement;
    expect(nav.textContent).toContain('Serviços');
    expect(nav.textContent).toContain('Artigos Científicos');

    const toggle = fixture.nativeElement.querySelector(
      '.lang-dropdown__toggle',
    ) as HTMLButtonElement;
    toggle.click();
    fixture.detectChanges();

    const options = Array.from(
      fixture.nativeElement.querySelectorAll('.lang-dropdown__option'),
    ) as HTMLButtonElement[];
    expect(options.length).toBe(2);
    expect(options[1].textContent).toContain('English');
    options[1].click();
    fixture.detectChanges();

    expect(nav.textContent).toContain('Services');
    expect(nav.textContent).toContain('Scientific Articles');
    expect(nav.textContent).not.toContain('Serviços');
    expect(toggle.textContent).toContain('English');
  });
});
