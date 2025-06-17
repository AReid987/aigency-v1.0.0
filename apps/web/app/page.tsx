import { Navigation } from "./components/Navigation";
import { HeroSection } from "./components/HeroSection";
import { FeaturesSection } from "./components/FeaturesSection";
import { StatsSection } from "./components/StatsSection";

export default function Home() {
  return (
    <main
      className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900"
      data-oid="a1nbdm2"
    >
      <Navigation data-oid="8av:mvx" />
      <HeroSection data-oid="ie9p8mi" />
      <StatsSection data-oid="5zr-vw9" />
      <FeaturesSection data-oid="pnhqi6-" />
    </main>
  );
}
