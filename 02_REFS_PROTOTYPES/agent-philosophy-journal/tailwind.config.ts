import type { Config } from "tailwindcss";

export default {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./app/**/*.{ts,tsx}",
    "./src/**/*.{ts,tsx}",
  ],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "#6E59A5",
          hover: "#9b87f5",
          foreground: "#ffffff",
        },
        secondary: {
          DEFAULT: "#0EA5E9",
          hover: "#38BDF8",
          foreground: "#ffffff",
        },
        accent: {
          DEFAULT: "#D946EF",
          foreground: "#ffffff",
        },
        card: {
          DEFAULT: "rgba(26, 31, 44, 0.8)",
          foreground: "#ffffff",
        },
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
        display: ["Space Grotesk", "sans-serif"],
      },
      boxShadow: {
        glow: "0 0 20px -5px rgba(110, 89, 165, 0.5)",
        "glow-strong": "0 0 30px -5px rgba(110, 89, 165, 0.8)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
} satisfies Config;