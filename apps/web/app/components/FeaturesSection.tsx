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
    <section id="features" className="px-6 py-20" data-oid="9ryfz52">
      <div className="mx-auto max-w-6xl" data-oid=":7j.ggh">
        {/* Built Around Section */}
        <div className="text-center mb-16" data-oid="wj6t7tu">
          <h2
            className="text-3xl md:text-4xl font-bold text-white mb-4"
            data-oid="xu5oo.e"
          >
            Built Around What You Need
          </h2>
          <p
            className="text-slate-400 text-lg max-w-2xl mx-auto"
            data-oid="2pe2o0d"
          >
            Everything you need to transform from solo founder to scaling
            entrepreneur
          </p>
        </div>

        <div
          className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-20"
          data-oid="q174gdh"
        >
          {features.map((feature, index) => (
            <div
              key={index}
              className="bg-slate-800/30 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-8 hover:border-teal-500/30 transition-all duration-300 hover:bg-slate-800/50"
              data-oid="oacqrzu"
            >
              <div className="text-4xl mb-4" data-oid="a1pbjdl">
                {feature.icon}
              </div>
              <h3
                className="text-xl font-semibold text-white mb-3"
                data-oid="h:phbr0"
              >
                {feature.title}
              </h3>
              <p className="text-slate-400 leading-relaxed" data-oid="qcnuqkm">
                {feature.description}
              </p>
            </div>
          ))}
        </div>

        {/* Problems We're Solving */}
        <div className="text-center mb-12" data-oid="_2gpew1">
          <h2
            className="text-3xl md:text-4xl font-bold text-white mb-8"
            data-oid="s8:n0kz"
          >
            We're Solving
          </h2>
          <div
            className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto"
            data-oid="puboh18"
          >
            {problems.map((problem, index) => (
              <div
                key={index}
                className="flex items-center space-x-3 bg-red-500/10 border border-red-500/20 rounded-lg p-4"
                data-oid="twdqipr"
              >
                <div
                  className="w-2 h-2 bg-red-400 rounded-full flex-shrink-0"
                  data-oid="ju04zk3"
                ></div>
                <span className="text-slate-300" data-oid="f6287rf">
                  {problem}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Final CTA */}
        <div
          className="text-center bg-gradient-to-r from-teal-500/10 to-teal-600/10 border border-teal-500/20 rounded-2xl p-12"
          data-oid="ub21egb"
        >
          <h3
            className="text-2xl md:text-3xl font-bold text-white mb-4"
            data-oid="eaxs_wl"
          >
            This isn't just a SaaS — it's a founder workflow transformer.
          </h3>
          <p
            className="text-slate-400 mb-8 max-w-2xl mx-auto"
            data-oid="amyivd7"
          >
            Join the next generation of entrepreneurs who are scaling faster
            with AI-native workflows.
          </p>
          <button
            className="bg-teal-500 hover:bg-teal-600 text-white px-8 py-4 rounded-lg font-semibold text-lg transition-colors"
            data-oid="_erro4j"
          >
            Transform Your Workflow
          </button>
        </div>
      </div>
    </section>
  );
}
