import { Hero } from "@/components/Hero";
import { FeaturedArticles } from "@/components/FeaturedArticles";
import { Navbar } from "@/components/Navbar";

const Index = () => {
  return (
    <div className="min-h-screen dark">
      <Navbar />
      <main>
        <Hero />
        <FeaturedArticles />
      </main>
    </div>
  );
};

export default Index;