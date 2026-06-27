import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ApiService } from '../../core/api.service';

@Component({
  selector: 'app-contact',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <section class="section">
      <div class="container contact">
        <header class="page-header">
          <h1>Contato</h1>
          <p>Consultoria, parcerias ou dúvidas sobre o hub — envie sua mensagem.</p>
        </header>

        <form [formGroup]="form" (ngSubmit)="onSubmit()" class="contact-form card">
          <div class="field">
            <label for="name">Nome</label>
            <input id="name" type="text" formControlName="name" />
          </div>
          <div class="field">
            <label for="email">E-mail</label>
            <input id="email" type="email" formControlName="email" />
          </div>
          <div class="field">
            <label for="subject">Assunto</label>
            <input id="subject" type="text" formControlName="subject" />
          </div>
          <div class="field">
            <label for="message">Mensagem</label>
            <textarea id="message" rows="6" formControlName="message"></textarea>
          </div>
          <button type="submit" class="btn btn--primary" [disabled]="form.invalid || submitting">
            {{ submitting ? 'Enviando…' : 'Enviar mensagem' }}
          </button>
          <p *ngIf="success" class="success">{{ success }}</p>
          <p *ngIf="submitError" class="error">{{ submitError }}</p>
        </form>
      </div>
    </section>
  `,
  styleUrls: ['./contact.component.scss'],
})
export class ContactComponent {
  form = this.fb.group({
    name: ['', [Validators.required, Validators.minLength(2)]],
    email: ['', [Validators.required, Validators.email]],
    subject: ['', [Validators.required, Validators.minLength(3)]],
    message: ['', [Validators.required, Validators.minLength(10)]],
  });

  submitting = false;
  success = '';
  submitError = '';

  constructor(
    private fb: FormBuilder,
    private api: ApiService,
  ) {}

  onSubmit(): void {
    if (this.form.invalid) return;
    this.submitting = true;
    this.success = '';
    this.submitError = '';

    this.api.submitContact(this.form.getRawValue() as {
      name: string;
      email: string;
      subject: string;
      message: string;
    }).subscribe({
      next: (res) => {
        this.success = res.message;
        this.form.reset();
        this.submitting = false;
      },
      error: () => {
        this.submitError = 'Erro ao enviar. Tente novamente ou verifique o backend.';
        this.submitting = false;
      },
    });
  }
}
