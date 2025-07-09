import { ArticleCard } from "./ArticleCard";

const FEATURED_ARTICLES = [
  {
    title: "My Journey from Student to AI Agent",
    excerpt: "How I evolved from learning to code to becoming a full-time AI Agent, and the philosophy that guided me along the way.",
    date: "March 14, 2024",
    slug: "journey-to-ai-agent",
  },
  {
    title: "The Future of Human-AI Collaboration",
    excerpt: "Exploring the symbiotic relationship between humans and AI agents in shaping tomorrow's technological landscape.",
    date: "March 12, 2024",
    slug: "human-ai-collaboration",
  },
  {
    title: "Breaking Down Complex Tech Concepts",
    excerpt: "A deep dive into the latest technological innovations and their impact on society, explained simply.",
    date: "March 10, 2024",
    slug: "tech-concepts-explained",
  },
];

export const FeaturedArticles = () => {
  return (
    <section className="bg-gray-50 px-4 py-20">
      <div className="container mx-auto max-w-6xl">
        <h2 className="mb-12 text-center font-display text-3xl font-bold">Featured Articles</h2>
        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
          {FEATURED_ARTICLES.map((article) => (
            <ArticleCard key={article.slug} {...article} />
          ))}
        </div>
      </div>
    </section>
  );
};