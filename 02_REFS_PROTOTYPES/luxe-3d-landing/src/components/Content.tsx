export const Content = () => {
  return (
    <section className="py-20 bg-white" id="about">
      <div className="container mx-auto px-6">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-neutral-dark mb-6">
            Curated Miniature Excellence
          </h2>
          <p className="text-neutral text-lg mb-12">
            We specialize in discovering and presenting the finest miniature art pieces from around the world. Each piece is carefully selected for its exceptional craftsmanship and artistic value.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            {features.map((feature, index) => (
              <div key={index} className="text-center">
                <h3 className="text-xl font-semibold text-neutral-dark mb-4">
                  {feature.title}
                </h3>
                <p className="text-neutral">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

const features = [
  {
    title: "Expert Curation",
    description: "Each piece is hand-selected by our team of art experts.",
  },
  {
    title: "Premium Quality",
    description: "We ensure the highest standards of craftsmanship and materials.",
  },
  {
    title: "Limited Editions",
    description: "Exclusive pieces available only through our collection.",
  },
];