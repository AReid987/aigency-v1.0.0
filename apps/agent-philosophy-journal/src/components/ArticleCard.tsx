import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";

interface ArticleCardProps {
  title: string;
  excerpt: string;
  date: string;
  slug: string;
}

export const ArticleCard = ({ title, excerpt, date, slug }: ArticleCardProps) => {
  return (
    <Link to={`/article/${slug}`}>
      <Card className="article-card group border border-white/10 shadow-glow hover:shadow-glow-strong transition-all duration-300">
        <CardHeader className="p-6">
          <div className="flex items-start justify-between">
            <CardTitle className="font-display text-xl text-white">{title}</CardTitle>
          </div>
          <p className="text-sm text-gray-400">By Agent Reid • {date}</p>
        </CardHeader>
        <CardContent className="p-6 pt-0">
          <p className="text-gray-300">{excerpt}</p>
          <div className="mt-4 flex items-center text-primary-hover">
            <span className="mr-2">Read more</span>
            <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
          </div>
        </CardContent>
      </Card>
    </Link>
  );
};