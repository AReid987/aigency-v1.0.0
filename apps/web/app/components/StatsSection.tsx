"use client";

export function StatsSection() {
  const stats = [
    { value: "$1.8M+", label: "Revenue Generated" },
    { value: "10,000+", label: "Active Users" },
    { value: "$349.50K", label: "Average ROI" },
  ];

  return (
    <section className="px-6 py-16" data-oid="7tlepbd">
      <div className="mx-auto max-w-6xl" data-oid="rk6d2zm">
        <div
          className="grid grid-cols-1 md:grid-cols-3 gap-8"
          data-oid="056h2xb"
        >
          {stats.map((stat, index) => (
            <div key={index} className="text-center" data-oid="7d85xzd">
              <div
                className="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-8 hover:border-teal-500/30 transition-colors"
                data-oid="h7tzj0m"
              >
                <div
                  className="text-3xl md:text-4xl font-bold text-white mb-2"
                  data-oid="clkr7x5"
                >
                  {stat.value}
                </div>
                <div
                  className="text-slate-400 text-sm uppercase tracking-wide"
                  data-oid="k4v2qyx"
                >
                  {stat.label}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
