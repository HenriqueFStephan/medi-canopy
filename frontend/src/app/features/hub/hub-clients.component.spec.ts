import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HubClientsComponent } from './hub-clients.component';
import { HUB_CLIENTS } from './hub.data';

describe('HubClientsComponent', () => {
  let fixture: ComponentFixture<HubClientsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HubClientsComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(HubClientsComponent);
    fixture.detectChanges();
  });

  it('shows the clients section title', () => {
    const title = fixture.nativeElement.querySelector('#hub-clients-title');
    expect(title?.textContent?.trim()).toBe('Clientes Medi Canopy');
  });

  it('shows an empty state when there are no clients', () => {
    expect(HUB_CLIENTS.length).toBe(0);
    const empty = fixture.nativeElement.querySelector('.hub-empty');
    expect(empty).withContext('empty state message').toBeTruthy();
  });
});
