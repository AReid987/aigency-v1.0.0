import type { Metadata, Viewport } from "next";
import { Toaster } from "../src/components/ui/toaster";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "Aigency",
    template: "%s | Aigency",
  },
  description:
    "Teams of agents that rock with you. An AI-native co-founder alternative for solo entrepreneurs and creatives.",
  keywords: [
    "AI",
    "automation",
    "entrepreneurs",
    "workflow",
    "agents",
    "productivity",
  ],

  authors: [{ name: "Aigency" }],
  metadataBase: new URL("https://aigency.com"),
  openGraph: {
    title: "Aigency - 10x Yourself with AI-Native Workflows",
    description:
      "Teams of agents that rock with you. An AI-native co-founder alternative for solo entrepreneurs and creatives.",
    url: "https://aigency.com",
    siteName: "Aigency",
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Aigency - 10x Yourself with AI-Native Workflows",
    description:
      "Teams of agents that rock with you. An AI-native co-founder alternative for solo entrepreneurs and creatives.",
    creator: "@aigency",
  },
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "white" },
    { media: "(prefers-color-scheme: dark)", color: "black" },
  ],

  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
};

import { ClerkProvider } from "@clerk/nextjs";
import { dark } from "@clerk/themes";


export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClerkProvider
      publishableKey={process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY!}
      appearance={{
        baseTheme: dark,
      }}
      data-oid="_7wpbm_"
    >
      <html
        lang="en"
        suppressHydrationWarning
        className="dark min-h-screen"
         data-oid="_8cle84"
       >
        <head>
          <link href="https://api.fontshare.com/v2/css?f[]=chillax@400,500,600,700&f[]=zodiak@300,400,500,600,700&display=swap" rel="stylesheet" />
        </head>
         <body
           className={`antialiased min-h-screen`}
           data-oid="a55bw97"
         >
           {children}
           <Toaster data-oid="9806pw6" />
        </body>
      </html>
    </ClerkProvider>
  );
}
