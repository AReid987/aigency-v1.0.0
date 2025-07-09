import type { Metadata } from "next";
import localFont from "next/font/local";
import Image from "next/image";
import "./globals.css";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
});

const plusJakartaSans = localFont({
  src: "./fonts/PlusJakartaSans-Variable.woff",
  variable: "--font-jakarta-variable",
});

const zodiakVariable = localFont({
  src: "./fonts/Zodiak-Variable.woff",
  variable: "--font-zodiak-variable",
});

import React from "react"; // Import React

export const metadata: Metadata = {
  title: "devLog XPRT",
  description: "Intel Ops",
};

export default async function RootLayout({
  children,
  ...props
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body
        className={`
          ${plusJakartaSans.variable} 
          ${zodiakVariable.variable}
        `}
      >
        {children}
      </body>
    </html>
  );
}
