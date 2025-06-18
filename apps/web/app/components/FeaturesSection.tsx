"use client";

export function FeaturesSection() {
  const features = [
    {
      title: "Agentic Squads",
      description:
        "Teams of specialized AI agents that co-create with you, each bringing unique expertise to your projects.",
      icon: "🤖",
    },
    {
      title: "Infinite Canvas",
      description:
        "Visual workspace for linked thinking, connecting ideas, strategies, and execution in one seamless flow.",
      icon: "🎨",
    },
    {
      title: "KPI Dashboards",
      description:
        "Real-time analytics and atomic systems that track what matters most for your business growth.",
      icon: "📊",
    },
    {
      title: "GTM Automations",
      description:
        "Marketing campaigns and go-to-market automations that scale your reach without the overhead.",
      icon: "🚀",
    },
  ];

  const problems = [
    "Overload of tools and docs",
    "Slow/misaligned GTM",
    "LLM unreliability for business-critical workflows",
    "Creative isolation",
  ];

  return (
    <section id="features" className="px-6 py-20 bg-slate-900" data-oid="bgv7rtz">
      <div className="mx-auto max-w-6xl" data-oid="s7zjl17">
        {/* Features Section */}
        <div className="text-center mb-16" data-oid="aoo0x0d">
          <h2
            className="text-3xl md:text-4xl font-bold text-white mb-4"
            data-oid="3hpypzq"
          >
            Built Around What You Need
          </h2>
          <p
            className="text-slate-400 text-lg max-w-2xl mx-auto"
            data-oid="tozsklt"
          >
            Everything you need to transform from solo founder to scaling
            entrepreneur
          </p>
        </div>

        <div
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-20"
          data-oid="mu_4ebo"
        >
          {features.map((feature, index) => (
            <div
              key={index}
              className="bg-gradient-to-br from-slate-800/40 to-slate-900/60 backdrop-blur-sm border border-slate-700/50 rounded-xl p-8 transition-all duration-300 hover:border-teal-500/50 hover:shadow-lg hover:shadow-teal-500/10"
              data-oid="6xyb-s3"
            >
              <div className="w-16 h-16 rounded-full bg-teal-500/10 flex items-center justify-center text-3xl mb-6 mx-auto" data-oid="c9pi-j4">
                {feature.icon}
              </div>
              <h3
                className="text-xl font-bold text-white mb-3 text-center"
                data-oid="rw9-yno"
              >
                {feature.title}
              </h3>
              <p className="text-slate-400 leading-relaxed text-center" data-oid="93lxaaj">
                {feature.description}
              </p>
            </div>
          ))}
        </div>

        {/* Problems We're Solving */}
        <div className="text-center mb-16" data-oid="w6d3ddf">
          <h2
            className="text-3xl md:text-4xl font-bold text-white mb-8"
            data-oid="74sb7a-"
          >
            We&apos;re Solving
          </h2>
          <div
            className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto"
            data-oid="-7xxnsi"
          >
            {problems.map((problem, index) => (
              <div
                key={index}
                className="flex items-start space-x-4 bg-gradient-to-r from-red-500/10 to-red-600/10 border border-red-500/20 rounded-xl p-5 text-left"
                data-oid="4s3f1iw"
              >
                <div
                  className="w-6 h-6 rounded-full bg-red-500 flex items-center justify-center flex-shrink-0 mt-1"
                  data-oid="8kyan9h"
                >
                  <div className="w-2 h-2 bg-white rounded-full"></div>
                </div>
                <span className="text-slate-300 font-medium" data-oid="iyhg_89">
                  {problem}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Final CTA */}
        <div
          className="text-center bg-gradient-to-r from-teal-500/10 via-teal-600/15 to-teal-500/10 border border-teal-500/30 rounded-2xl p-12 relative overflow-hidden"
          data-oid="6awoeag"
        >
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(94,234,212,0.1)_0%,transparent_70%)]"></div>
          <h3
            className="text-2xl md:text-3xl font-bold text-white mb-4 relative z-10"
            data-oid="j5c:kuk"
          >
            This isn&apos;t just a SaaS — it&apos;s a founder workflow transformer.
          </h3>
          <p
            className="text-slate-400 mb-8 max-w-2xl mx-auto relative z-10"
            data-oid="4p_d129"
          >
            Join the next generation of entrepreneurs who are scaling faster
            with AI-native workflows.
          </p>
          <button
            className="bg-gradient-to-r from-teal-500 to-teal-600 hover:from-teal-600 hover:to-teal-700 text-white px-8 py-4 rounded-lg font-bold text-lg transition-all duration-300 shadow-lg shadow-teal-500/20 hover:shadow-teal-500/30 relative z-10"
            data-oid="odzddbt"
          >
            Transform Your Workflow
          </button>
        </div>
      </div>
    </section>
  );
}
