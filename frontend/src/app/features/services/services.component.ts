import { Component, ElementRef, HostListener, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ApiService } from '../../core/api.service';
import { ServiceOffering } from '../../core/models';

@Component({
  selector: 'app-services',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <section class="section">
      <div class="container">
        <header class="page-header">
          <h1>Consultoria Técnica e Estratégica em Cannabis Medicinal</h1>
          <p>
            Visão integrada de toda a cadeia produtiva — da concepção e implantação da unidade ao cultivo,
            processamento e operação comercial.
          </p>
        </header>

        <div *ngIf="loading" class="loading">Carregando serviços…</div>
        <div *ngIf="error" class="error-state">{{ error }}</div>

        <ul class="feature-list" *ngIf="!loading && !error">
          <li *ngFor="let svc of services">
            <div>
              <h3>{{ displayTitle(svc.title) }}</h3>
              <p>{{ svc.description }}</p>
              <ul class="highlights" *ngIf="svc.highlights.length">
                <li *ngFor="let h of svc.highlights">{{ h }}</li>
              </ul>
            </div>
          </li>
        </ul>
      </div>
    </section>

    <section class="cta-minimal">
      <div class="container">
        <h2>Pronto para estruturar seu projeto?</h2>
        <p>Agende uma conversa para mapear instalação, climatização, cultivo e compliance.</p>
        <button type="button" class="btn btn--primary" (click)="openOverlay()">
          Solicitar consultoria
        </button>
      </div>
    </section>

    <div
      class="consulting-overlay"
      *ngIf="overlayOpen"
      (click)="closeOverlay()"
    >
      <div
        class="consulting-dialog card"
        role="dialog"
        aria-modal="true"
        aria-labelledby="consulting-title"
        (click)="$event.stopPropagation()"
      >
        <button
          type="button"
          class="consulting-dialog__close"
          (click)="closeOverlay()"
          aria-label="Fechar"
        >
          ×
        </button>
        <h2 id="consulting-title">Solicitar consultoria</h2>
        <p class="consulting-dialog__lead">
          Confirme os dados abaixo para enviar a solicitação à equipe.
        </p>

        <form [formGroup]="form" (ngSubmit)="onSubmit()" class="consulting-form" novalidate>
          <div class="field">
            <label for="consulting-name">Nome</label>
            <input
              #nameInput
              id="consulting-name"
              type="text"
              formControlName="name"
              autocomplete="name"
            />
          </div>
          <div class="field">
            <label for="consulting-email">E-mail</label>
            <input id="consulting-email" type="email" formControlName="email" autocomplete="email" />
          </div>
          <div class="field-row">
            <div class="field">
              <label for="consulting-company">Empresa <span class="optional">(opcional)</span></label>
              <input id="consulting-company" type="text" formControlName="company" autocomplete="organization" />
            </div>
            <div class="field">
              <label for="consulting-phone">Telefone <span class="optional">(opcional)</span></label>
              <input id="consulting-phone" type="tel" formControlName="phone" autocomplete="tel" />
            </div>
          </div>
          <fieldset class="field" [disabled]="!services.length">
            <legend>Áreas de interesse <span class="optional">(opcional)</span></legend>
            <ul class="interest-list">
              <li *ngFor="let svc of services">
                <label class="interest-option">
                  <input
                    type="checkbox"
                    [checked]="isSelected(svc.id)"
                    (change)="toggleService(svc.id, $event)"
                  />
                  <span>{{ displayTitle(svc.title) }}</span>
                </label>
              </li>
            </ul>
          </fieldset>
          <div class="field">
            <label for="consulting-message">Sobre o projeto</label>
            <textarea
              id="consulting-message"
              rows="5"
              formControlName="message"
              placeholder="Instalação, cultivo, compliance, prazos…"
            ></textarea>
          </div>
          <button type="submit" class="btn btn--primary" [disabled]="form.invalid || submitting">
            {{ submitting ? 'Enviando…' : 'Confirmar solicitação' }}
          </button>
          <p *ngIf="success" class="success" role="status">{{ success }}</p>
          <p *ngIf="submitError" class="error" role="alert">{{ submitError }}</p>
        </form>
      </div>
    </div>
  `,
  styleUrls: ['./services.component.scss'],
})
export class ServicesComponent implements OnInit, OnDestroy {
  @ViewChild('nameInput') nameInput?: ElementRef<HTMLInputElement>;

  services: ServiceOffering[] = [];
  loading = true;
  error = '';
  overlayOpen = false;
  submitting = false;
  success = '';
  submitError = '';
  selectedServiceIds: string[] = [];

  form = this.fb.group({
    name: ['', [Validators.required, Validators.minLength(2)]],
    email: ['', [Validators.required, Validators.email]],
    company: [''],
    phone: [''],
    message: ['', [Validators.required, Validators.minLength(10)]],
  });

  constructor(
    private api: ApiService,
    private fb: FormBuilder,
  ) {}

  /** CSS already numbers .feature-list rows; drop the same index from API titles. */
  displayTitle(title: string): string {
    return title.replace(/^\s*\d+\s*[—–−-]\s*/, '').trim();
  }

  isSelected(id: string): boolean {
    return this.selectedServiceIds.includes(id);
  }

  toggleService(id: string, event: Event): void {
    const checked = (event.target as HTMLInputElement).checked;
    if (checked) {
      if (!this.selectedServiceIds.includes(id)) {
        this.selectedServiceIds = [...this.selectedServiceIds, id];
      }
      return;
    }
    this.selectedServiceIds = this.selectedServiceIds.filter((item) => item !== id);
  }

  ngOnInit(): void {
    this.api.getServices().subscribe({
      next: (data) => {
        this.services = data;
        this.loading = false;
      },
      error: () => {
        this.error = 'Não foi possível carregar os serviços.';
        this.loading = false;
      },
    });
  }

  ngOnDestroy(): void {
    this.unlockPage();
  }

  @HostListener('document:keydown.escape')
  onEscape(): void {
    if (this.overlayOpen && !this.submitting) {
      this.closeOverlay();
    }
  }

  openOverlay(): void {
    this.success = '';
    this.submitError = '';
    this.overlayOpen = true;
    document.body.style.overflow = 'hidden';
    setTimeout(() => this.nameInput?.nativeElement.focus());
  }

  closeOverlay(): void {
    if (this.submitting) return;
    this.overlayOpen = false;
    this.unlockPage();
  }

  onSubmit(): void {
    if (this.form.invalid) return;
    this.submitting = true;
    this.success = '';
    this.submitError = '';

    const value = this.form.getRawValue();
    this.api.submitConsultingRequest({
      name: value.name ?? '',
      email: value.email ?? '',
      company: value.company?.trim() || undefined,
      phone: value.phone?.trim() || undefined,
      service_ids: this.selectedServiceIds,
      message: value.message ?? '',
    }).subscribe({
      next: (res) => {
        this.success = res.message;
        this.submitError = res.email_sent ? '' : (res.email_error || '');
        this.form.reset();
        this.selectedServiceIds = [];
        this.submitting = false;
      },
      error: (err) => {
        const detail = err?.error?.detail;
        this.submitError =
          typeof detail === 'string'
            ? detail
            : 'Erro ao enviar. Tente novamente ou verifique o backend.';
        this.submitting = false;
      },
    });
  }

  private unlockPage(): void {
    document.body.style.overflow = '';
  }
}
