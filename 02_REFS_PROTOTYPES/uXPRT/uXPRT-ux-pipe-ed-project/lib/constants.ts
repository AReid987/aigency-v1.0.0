import { MainNavItem, SidebarNavItem } from "@/lib/types";

export const siteConfig = {
  name: "ProductDocs Academy",
  description: "Learn how to create effective product documentation and improve your prompt engineering skills.",
  url: "https://productdocs.academy",
  ogImage: "https://productdocs.academy/og.jpg",
  links: {
    github: "https://github.com/yourusername/productdocs-academy",
  },
};

export const mainNav: MainNavItem[] = [
  {
    title: "Learn",
    href: "/learn",
    description: "Interactive modules to master product documentation"
  },
  {
    title: "Examples",
    href: "/examples",
    description: "Real-world examples of product documentation"
  },
  {
    title: "Resources",
    href: "/resources",
    description: "Additional resources and templates"
  },
];

export const learnSidebarNav: SidebarNavItem[] = [
  {
    title: "Getting Started",
    href: "/learn",
  },
  {
    title: "Go-to-Market",
    items: [
      {
        title: "GTM Template",
        href: "/learn/gtm-template",
      },
      {
        title: "GTM Plan",
        href: "/learn/gtm-plan",
      },
    ],
  },
  {
    title: "Product Documentation",
    items: [
      {
        title: "One Pager",
        href: "/learn/one-pager",
      },
      {
        title: "Product Strategy",
        href: "/learn/product-strategy",
      },
      {
        title: "Product Launch",
        href: "/learn/product-launch",
      },
    ],
  },
];