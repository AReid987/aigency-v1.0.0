
import LandingPage from "@/components/landing-page";
import ContactForm from "@/components/ui/contact-form";

export default function Home() {
  return (
    <main>
      <LandingPage />
      <section className="py-12">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-8">Contact Us</h2>
          <div className="max-w-md mx-auto">
            <ContactForm projectId="aigency-contact" />
          </div>
        </div>
      </section>
    </main>
  );
}
