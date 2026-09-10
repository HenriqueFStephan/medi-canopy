import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./features/home/home.component').then((m) => m.HomeComponent),
  },
  {
    path: 'news',
    loadComponent: () =>
      import('./features/news/news-list.component').then((m) => m.NewsListComponent),
  },
  {
    path: 'blog',
    loadComponent: () =>
      import('./features/blog/blog-list.component').then((m) => m.BlogListComponent),
  },
  {
    path: 'blog/:slug',
    loadComponent: () =>
      import('./features/blog/blog-detail.component').then((m) => m.BlogDetailComponent),
  },
  {
    path: 'courses',
    loadComponent: () =>
      import('./features/courses/courses.component').then((m) => m.CoursesComponent),
  },
  {
    path: 'services',
    loadComponent: () =>
      import('./features/services/services.component').then((m) => m.ServicesComponent),
  },
  {
    path: 'hub',
    loadComponent: () =>
      import('./features/hub/hub-layout.component').then((m) => m.HubLayoutComponent),
    children: [
      { path: '', redirectTo: 'parceiros', pathMatch: 'full' },
      {
        path: 'parceiros',
        loadComponent: () =>
          import('./features/hub/hub-partners.component').then((m) => m.HubPartnersComponent),
      },
      {
        path: 'clientes',
        loadComponent: () =>
          import('./features/hub/hub-clients.component').then((m) => m.HubClientsComponent),
      },
    ],
  },
  {
    path: 'contact',
    loadComponent: () =>
      import('./features/contact/contact.component').then((m) => m.ContactComponent),
  },
  { path: '**', redirectTo: '' },
];
