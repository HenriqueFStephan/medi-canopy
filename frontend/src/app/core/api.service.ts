import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';
import { I18nService } from './i18n';
import {
  BlogPost,
  ContactPayload,
  ContactResponse,
  ConsultingRequestPayload,
  ConsultingRequestResponse,
  Course,
  NewsArticle,
  ServiceOffering,
} from './models';

/**
 * HTTP client for Medi Canopy FastAPI backend.
 * All endpoints are versioned under /api/v1.
 */
@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly base = environment.apiUrl;

  constructor(
    private http: HttpClient,
    private i18n: I18nService,
  ) {}

  getNews(region?: string): Observable<NewsArticle[]> {
    let params = this.langParams();
    if (region) {
      params = params.set('region', region);
    }
    return this.http.get<NewsArticle[]>(`${this.base}/news`, { params });
  }

  getBlogPosts(tag?: string): Observable<BlogPost[]> {
    let params = this.langParams();
    if (tag) {
      params = params.set('tag', tag);
    }
    return this.http.get<BlogPost[]>(`${this.base}/blog`, { params });
  }

  getBlogBySlug(slug: string): Observable<BlogPost> {
    return this.http.get<BlogPost>(`${this.base}/blog/slug/${slug}`, {
      params: this.langParams(),
    });
  }

  getCourses(): Observable<Course[]> {
    return this.http.get<Course[]>(`${this.base}/courses`, { params: this.langParams() });
  }

  getServices(): Observable<ServiceOffering[]> {
    return this.http.get<ServiceOffering[]>(`${this.base}/services`, {
      params: this.langParams(),
    });
  }

  submitContact(payload: ContactPayload): Observable<ContactResponse> {
    return this.http.post<ContactResponse>(`${this.base}/contact`, payload, {
      params: this.langParams(),
    });
  }

  submitConsultingRequest(
    payload: ConsultingRequestPayload,
  ): Observable<ConsultingRequestResponse> {
    return this.http.post<ConsultingRequestResponse>(
      `${this.base}/services/consulting-request`,
      payload,
      { params: this.langParams() },
    );
  }

  private langParams(): HttpParams {
    return new HttpParams().set('lang', this.i18n.lang());
  }
}
