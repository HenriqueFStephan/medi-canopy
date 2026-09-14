import { BlogPost } from '../../core/models';

/** Filters blog posts by title only (case-insensitive substring match). */
export function filterBlogPostsByTitle(posts: BlogPost[], query: string): BlogPost[] {
  const normalized = query.trim().toLowerCase();
  if (!normalized) {
    return posts;
  }
  return posts.filter((post) => post.title.toLowerCase().includes(normalized));
}
