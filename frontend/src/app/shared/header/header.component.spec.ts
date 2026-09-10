import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { HeaderComponent } from './header.component';

describe('HeaderComponent', () => {
  let fixture: ComponentFixture<HeaderComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HeaderComponent],
      providers: [provideRouter([])],
    }).compileComponents();

    fixture = TestBed.createComponent(HeaderComponent);
    fixture.detectChanges();
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
});
