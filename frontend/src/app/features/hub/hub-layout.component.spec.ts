import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { I18nService } from '../../core/i18n';
import { HubLayoutComponent } from './hub-layout.component';
import { HubPartnersComponent } from './hub-partners.component';
import { HubClientsComponent } from './hub-clients.component';

describe('HubLayoutComponent', () => {
  let fixture: ComponentFixture<HubLayoutComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HubLayoutComponent],
      providers: [
        provideRouter([
          {
            path: 'hub',
            component: HubLayoutComponent,
            children: [
              { path: 'parceiros', component: HubPartnersComponent },
              { path: 'clientes', component: HubClientsComponent },
            ],
          },
        ]),
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(HubLayoutComponent);
    TestBed.inject(I18nService).setLang('pt-BR');
    fixture.detectChanges();
  });

  it('renders the Hub title and lead description', () => {
    const title = fixture.nativeElement.querySelector('h1');
    const lead = fixture.nativeElement.querySelector('.hub-page__lead');

    expect(title?.textContent?.trim()).toBe('Hub');
    expect(lead?.textContent?.trim()).toBe(
      'Conheça o ecossistema Medi Canopy, que reúne associações, empresas e parceiros estratégicos envolvidos em cuidado, pesquisa, tecnologia, regulação, jurídico e compliance no universo da cannabis medicinal.'
    );
  });

  it('renders Hub navigation links for Parceiros and Clientes', () => {
    const links = Array.from(
      fixture.nativeElement.querySelectorAll('.hub-nav__link')
    ) as HTMLAnchorElement[];

    expect(links.length).toBe(2);
    expect(links[0].textContent?.trim()).toBe('Parceiros');
    expect(links[0].getAttribute('href')).toBe('/hub/parceiros');
    expect(links[1].textContent?.trim()).toBe('Clientes');
    expect(links[1].getAttribute('href')).toBe('/hub/clientes');
  });
});
