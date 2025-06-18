"use client";

export function StatsSection() {
  const stats = [
    { value: "$1.8M+", label: "Revenue Generated" },
    { value: "10,000+", label: "Active Users" },
    { value: "$349.50K", label: "Average ROI" },
  ];

  return (
    <section className="px-6 py-16" data-oid="o_vv:qq">
      <div className="mx-auto max-w-6xl" data-oid="_nj7c7j">
        <div
          className="grid grid-cols-1 md:grid-cols-3 gap-8"
          data-oid="ijhksx2"
        >
          {stats.map((stat, index) => (
            <div key={index} className="text-center" data-oid="8cfr:4i">
              <div
                className="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-8 hover:border-teal-500/30 transition-colors"
                data-oid="1m0:yc0"
              >
                <div
                  className="text-3xl md:text-4xl font-bold text-white mb-2"
                  data-oid="or.7-i."
                >
                  {stat.value}
                </div>
                <div
                  className="text-slate-400 text-sm uppercase tracking-wide"
                  data-oid="-g4e77o"
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
