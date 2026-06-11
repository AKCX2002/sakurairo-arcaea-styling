import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

const SITE = "https://babel36acl.xyz";
const OUT_DIR = path.resolve("src/data");

async function fetchJson(url) {
  const response = await fetch(url, {
    headers: {
      "User-Agent": "babel36acl-astro-migrator/0.1"
    }
  });

  if (!response.ok) {
    throw new Error(`GET ${url} failed: ${response.status} ${response.statusText}`);
  }

  return {
    data: await response.json(),
    totalPages: Number(response.headers.get("x-wp-totalpages") || "1")
  };
}

async function fetchAll(type, fields) {
  const firstUrl = `${SITE}/wp-json/wp/v2/${type}?per_page=100&page=1&_fields=${fields}`;
  const first = await fetchJson(firstUrl);
  const items = [...first.data];

  for (let page = 2; page <= first.totalPages; page += 1) {
    const url = `${SITE}/wp-json/wp/v2/${type}?per_page=100&page=${page}&_fields=${fields}`;
    const next = await fetchJson(url);
    items.push(...next.data);
  }

  return items;
}

function textFromRendered(value) {
  return String(value?.rendered || "")
    .replace(/<[^>]*>/g, "")
    .replace(/&hellip;/g, "...")
    .replace(/&#8230;/g, "...")
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .trim();
}

function cleanHtml(html) {
  return String(html || "")
    .replaceAll(SITE, "")
    .replaceAll("https://www.babel36acl.xyz", "")
    .replace(/<script[\s\S]*?<\/script>/gi, "")
    .replace(/<style[\s\S]*?<\/style>/gi, "");
}

function decodeSlug(slug) {
  try {
    return decodeURIComponent(slug);
  } catch {
    return slug;
  }
}

function postRoute(post) {
  const date = new Date(post.date);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}/${month}/${day}/${decodeSlug(post.slug)}`;
}

function pageRoute(page) {
  return decodeSlug(page.slug);
}

function byNameMap(items) {
  return Object.fromEntries(items.map((item) => [item.id, item.name]));
}

async function main() {
  await mkdir(OUT_DIR, { recursive: true });

  const fields = [
    "id",
    "date",
    "modified",
    "slug",
    "link",
    "title",
    "excerpt",
    "content",
    "categories",
    "tags",
    "featured_media"
  ].join(",");

  const [posts, pages, categories, tags] = await Promise.all([
    fetchAll("posts", fields),
    fetchAll("pages", fields),
    fetchAll("categories", "id,name,slug,count,description"),
    fetchAll("tags", "id,name,slug,count,description")
  ]);

  const categoryNames = byNameMap(categories);
  const tagNames = byNameMap(tags);

  const migratedPosts = posts.map((post) => ({
    id: post.id,
    type: "post",
    route: postRoute(post),
    slug: decodeSlug(post.slug),
    sourceUrl: post.link,
    title: textFromRendered(post.title),
    excerpt: textFromRendered(post.excerpt),
    date: post.date,
    modified: post.modified,
    categories: (post.categories || []).map((id) => ({
      id,
      name: categoryNames[id] || String(id)
    })),
    tags: (post.tags || []).map((id) => ({
      id,
      name: tagNames[id] || String(id)
    })),
    content: cleanHtml(post.content?.rendered)
  }));

  const migratedPages = pages.map((page) => ({
    id: page.id,
    type: "page",
    route: pageRoute(page),
    slug: decodeSlug(page.slug),
    sourceUrl: page.link,
    title: textFromRendered(page.title),
    excerpt: textFromRendered(page.excerpt),
    date: page.date,
    modified: page.modified,
    content: cleanHtml(page.content?.rendered)
  }));

  const site = {
    source: SITE,
    migratedAt: new Date().toISOString(),
    title: "Babel36acl 的个人博客",
    description: "嵌入式实战、工程复盘、架构重构、工具实践与生活记录。",
    counts: {
      posts: migratedPosts.length,
      pages: migratedPages.length,
      categories: categories.length,
      tags: tags.length
    }
  };

  await Promise.all([
    writeFile(path.join(OUT_DIR, "posts.json"), JSON.stringify(migratedPosts, null, 2)),
    writeFile(path.join(OUT_DIR, "pages.json"), JSON.stringify(migratedPages, null, 2)),
    writeFile(path.join(OUT_DIR, "categories.json"), JSON.stringify(categories, null, 2)),
    writeFile(path.join(OUT_DIR, "tags.json"), JSON.stringify(tags, null, 2)),
    writeFile(path.join(OUT_DIR, "site.json"), JSON.stringify(site, null, 2))
  ]);

  console.log(`Migrated ${migratedPosts.length} posts, ${migratedPages.length} pages.`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
