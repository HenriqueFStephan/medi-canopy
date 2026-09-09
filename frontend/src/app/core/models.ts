/**
 * Shared TypeScript interfaces mirroring backend Pydantic schemas.
 */

export interface NewsArticle {
  id: string;
  title: string;
  summary: string;
  content: string;
  source_url?: string;
  source_name?: string;
  region: string;
  tags: string[];
  published_at?: string;
}

export interface BlogPost {
  id: string;
  title: string;
  slug: string;
  excerpt: string;
  content_markdown: string;
  tags: string[];
  source_type: string;
  cover_image_url?: string;
  instagram_url?: string;
  citation?: string;
  author_name: string;
  published_at: string;
}

export interface Course {
  id: string;
  title: string;
  slug: string;
  description: string;
  level: string;
  price_display: string;
  cover_image_url?: string;
  modules: { title: string; description: string; duration_minutes: number }[];
  published: boolean;
  coming_soon: boolean;
}

export interface ServiceOffering {
  id: string;
  title: string;
  description: string;
  icon: string;
  highlights: string[];
}

export interface ContactPayload {
  name: string;
  email: string;
  subject: string;
  message: string;
}

export interface ContactResponse {
  success: boolean;
  message: string;
}

export interface ConsultingRequestPayload {
  name: string;
  email: string;
  company?: string;
  phone?: string;
  service_ids: string[];
  message: string;
}

export interface ConsultingRequestResponse {
  success: boolean;
  message: string;
  email_sent: boolean;
  email_error?: string | null;
}
