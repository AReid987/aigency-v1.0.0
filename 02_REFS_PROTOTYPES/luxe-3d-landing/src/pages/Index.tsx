import { Navbar } from "@/components/Navbar";
import { Hero } from "@/components/Hero";
import { Content } from "@/components/Content";

const Index = () => {
  return (
    <div className="min-h-screen bg-white">
      <Navbar />
      <Hero />
      <Content />
    </div>
  );
};

export default Index;