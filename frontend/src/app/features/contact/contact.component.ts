import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

import { ApiService } from '../../core/api.service';
import { TranslatePipe } from '../../core/i18n';

@Component({
  selector: 'app-contact',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, TranslatePipe],
  template: `
    <section class="section">
      <div class="container contact">
        <header class="page-header">
          <h1>{{ 'contact.title' | t }}</h1>
          <p>{{ 'contact.lead' | t }}</p>
        </header>

        <form [formGroup]="form" (ngSubmit)="onSubmit()" class="contact-form card">
          <div class="field">
            <label for="name">{{ 'contact.name' | t }}</label>
            <input id="name" type="text" formControlName="name" />
          </div>
          <div class="field">
            <label for="email">{{ 'contact.email' | t }}</label>
            <input id="email" type="email" formControlName="email" />
          </div>
          <div class="field">
            <label for="subject">{{ 'contact.subject' | t }}</label>
            <input id="subject" type="text" formControlName="subject" />
          </div>
          <div class="field">
            <label for="message">{{ 'contact.message' | t }}</label>
            <textarea id="message" rows="6" formControlName="message"></textarea>
          </div>
          <button type="submit" class="btn btn--primary" [disabled]="form.invalid || submitting">
            {{ submitting ? ('contact.submitting' | t) : ('contact.submit' | t) }}
          </button>
          <p *ngIf="success" class="success">{{ success | t }}</p>
          <p *ngIf="submitError" class="error">{{ submitError | t }}</p>
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
  success: '' | 'contact.success' = '';
  submitError: '' | 'contact.error' = '';

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
        this.success = res.success ? 'contact.success' : '';
        this.form.reset();
        this.submitting = false;
      },
      error: () => {
        this.submitError = 'contact.error';
        this.submitting = false;
      },
    });
  }
}
