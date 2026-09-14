import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';

import { ApiService } from '../../core/api.service';
import { I18nService } from '../../core/i18n';
import { BlogPost } from '../../core/models';
import { BlogListComponent } from './blog-list.component';

const mockPosts: BlogPost[] = [
  {
    id: '1',
    title: 'CBD clinical trial results',
    slug: 'cbd-trial',
    excerpt: 'THC mentioned in excerpt only',
    content_markdown: '',
    tags: [],
    source_type: 'agent_research',
    author_name: 'Author',
    published_at: '2026-01-01',
  },
  {
    id: '2',
    title: 'Industrial hemp yield study',
    slug: 'hemp-yield',
    excerpt: '',
    content_markdown: '',
    tags: [],
    source_type: 'manual',
    author_name: 'Author',
    published_at: '2026-01-02',
  },
];

describe('BlogListComponent', () => {
  let fixture: ComponentFixture<BlogListComponent>;
  let api: jasmine.SpyObj<ApiService>;

  beforeEach(async () => {
    api = jasmine.createSpyObj<ApiService>('ApiService', ['getBlogPosts']);
    api.getBlogPosts.and.returnValue(of(mockPosts));

    await TestBed.configureTestingModule({
      imports: [BlogListComponent],
      providers: [{ provide: ApiService, useValue: api }],
    }).compileComponents();

    fixture = TestBed.createComponent(BlogListComponent);
    TestBed.inject(I18nService).setLang('pt-BR');
    fixture.detectChanges();
  });

  it('renders the search field to the right of the section description', () => {
    const header = fixture.nativeElement.querySelector('.blog-page-header');
    const intro = header?.querySelector('.blog-page-header__intro');
    const search = header?.querySelector('.blog-page-header__search input');

    expect(header).toBeTruthy();
    expect(intro?.querySelector('h1')?.textContent?.trim()).toBe('Ciência & Cannabis');
    expect(search?.getAttribute('type')).toBe('search');
  });

  it('filters posts by title in real time', () => {
    const input: HTMLInputElement = fixture.nativeElement.querySelector('#blog-search');
    input.value = 'cbd';
    input.dispatchEvent(new Event('input'));
    fixture.detectChanges();

    const titles = Array.from(fixture.nativeElement.querySelectorAll('.col-title')).map(
      (node: Element) => node.textContent?.trim(),
    );
    expect(titles).toEqual(['CBD clinical trial results']);
  });

  it('shows all posts again when the search is cleared', () => {
    const input: HTMLInputElement = fixture.nativeElement.querySelector('#blog-search');

    input.value = 'cbd';
    input.dispatchEvent(new Event('input'));
    fixture.detectChanges();

    input.value = '';
    input.dispatchEvent(new Event('input'));
    fixture.detectChanges();

    expect(fixture.nativeElement.querySelectorAll('.news-row').length).toBe(2);
  });

  it('shows an empty-state message when no title matches', () => {
    const input: HTMLInputElement = fixture.nativeElement.querySelector('#blog-search');
    input.value = 'inexistente';
    input.dispatchEvent(new Event('input'));
    fixture.detectChanges();

    const empty = fixture.nativeElement.querySelector('.blog-empty');
    expect(empty?.textContent?.trim()).toBe('Nenhum artigo encontrado para a busca.');
    expect(fixture.nativeElement.querySelectorAll('.news-row').length).toBe(0);
  });
});
