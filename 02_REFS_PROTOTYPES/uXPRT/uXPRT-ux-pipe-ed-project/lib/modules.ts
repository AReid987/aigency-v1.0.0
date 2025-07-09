import { Module } from "@/lib/types";

export const modules: Module[] = [
  {
    id: "gtm",
    title: "Go-to-Market Strategy",
    description: "Learn how to create effective go-to-market plans and templates to launch your product successfully.",
    coverImage: "https://images.pexels.com/photos/3184360/pexels-photo-3184360.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    documents: [
      {
        title: "GTM Template",
        description: "A comprehensive template for planning your product launch",
        href: "/learn/gtm/gtm-template",
        icon: "rocket",
        content: `# GTM Template

**Launch Plan for [SaaS Product Name]**
*Accelerate adoption, build buzz, and drive conversions with a strategic rollout.*

---

### **Phase 1: Pre-Launch Preparation (6–8 Weeks Before Launch)**

**Objective:** Build anticipation, validate the product, and secure early adopters.

#### **1. Market & Audience Alignment**

- **Audience Segmentation:** Define ICP (Ideal Customer Profile) and user personas (e.g., SMBs, enterprise teams, freelancers).

- **Competitor Analysis:** Identify gaps in competitors' offerings to highlight your unique advantages.

- **Beta Testing:** Invite 50–100 target users for feedback. Use tools like *Hotjar* or *UserTesting* to track behavior.

#### **2. Positioning & Messaging**

- **Core Value Proposition:** Craft a one-liner (e.g., "Slack for remote construction teams").

- **Key Messaging Pillars:** Focus on pain points (e.g., "Stop wasting hours on manual data entry").

- **Brand Assets:** Develop a press kit, case studies (if available), and demo videos.`
      },
      {
        title: "GTM Plan",
        description: "A structured approach to defining your go-to-market strategy",
        href: "/learn/gtm/gtm-plan",
        icon: "target",
        content: `# GTM Plan

## Go-to-Market Plan

### Executive Summary

Brief summary of the go-to-market strategy (e.g., "This plan outlines the strategy for launching our AI chatbot to increase user adoption and engagement.")

### Market Analysis

In-depth analysis of the target market (e.g., "Targeting small to medium-sized businesses in tech-savvy sectors.")

### Product Positioning

How the product will be positioned in the market (e.g., "Positioned as an easy-to-use, highly responsive customer support solution.")

### Pricing Strategy

Pricing model for the product (e.g., "Subscription-based model with tiered pricing.")

### Promotional Plan

Marketing and promotional activities (e.g., "Social media campaigns, Content marketing, Webinars")

### Sales Strategy

Sales tactics and channels (e.g., "Direct sales team, Partnerships with support software providers")

### Success Metrics

Key metrics for measuring the success of the launch (e.g., "User acquisition targets, Conversion rates, Revenue milestones")`
      }
    ]
  },
  {
    id: "product-docs",
    title: "Product Documentation",
    description: "Discover how to create clear, effective product documentation that communicates value and guides development.",
    coverImage: "https://images.pexels.com/photos/3182773/pexels-photo-3182773.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    documents: [
      {
        title: "One Pager",
        description: "Concise communication of product concepts and value",
        href: "/learn/product-docs/one-pager",
        icon: "file-text",
        content: `# One Pager

## Description

What is the product? This is just a brief description of what you're thinking, so that folks reading this doc can quickly grok what this project is all about. Keep it brief.

### Problem

Think of the problem like a hypothesis. What do you believe the problem you are solving is, and why? You'll add more context later. Key attributes of a strong problem statement include: It's short. Aim for a single sentence to describe the actual problem. The more you need to explain it, the less clear the problem ends up being. It's focused. It includes just a single clear problem that can be owned by a single team and solved in a reasonable amount of time. It's often very helpful to add some examples of what problem you are *not* solving. It references a "need" that is not being fulfilled. Try to focus this around a user need, but can also be a business need if necessary. The Jobs-To-Be-Done framework is especially useful here. It includes a what and a why. What's going wrong, and why is it a problem? You'll need to back this up in the next section. It's agnostic of a solution. Resist the urge to jump to a solution this early.`
      },
      {
        title: "Product Strategy",
        description: "Comprehensive guide to product strategy development",
        href: "/learn/product-docs/product-strategy",
        icon: "lightbulb",
        content: `# Product Strategy

## Product Strategy Document

### Product Vision and Mission

Define the overarching purpose and long-term impact of your product. Your Product Vision and Mission steer your strategy, providing focus and meaning.

### Product Vision

Articulate the future state or ultimate aspiration of your product. It should be compelling and align with your company's broader vision.

### Product Mission

Convey what your product aims to achieve for its users and how it contributes to realizing your Product Vision.

### Market Analysis

Gain a deep understanding of your market landscape. Identify industry trends, evaluate competitors, analyze your target audience, and pinpoint opportunities and threats.`
      },
      {
        title: "Product Launch",
        description: "Checklist for successful product launches",
        href: "/learn/product-docs/product-launch",
        icon: "rocket",
        content: `# Product Launch

## Product Launch Checklist

### Pre-Launch Activities

Tasks to complete before the launch (e.g., "Finalize product features, Complete beta testing, Develop marketing materials")

### Marketing Materials

Essential marketing assets (e.g., "Product one-pager, Social media posts, Press release")

### Sales Enablement

Tools and training for the sales team (e.g., "Sales demo video, Training sessions, Sales playbook")

### Training

Internal and customer training efforts (e.g., "Product training for support team, User guides for customers")

### Technical Readiness

Ensuring the product's technical aspects are ready (e.g., "Scalability tests, Performance optimization, Bug fixes")

### Post-Launch Monitoring

Monitoring and adjusting post-launch (e.g., "Monitor user feedback, Track key performance metrics, Rollout updates")`
      }
    ]
  },
  {
    id: "technical-docs",
    title: "Technical Documentation",
    description: "Learn how to create clear and effective technical documentation for developers and API users.",
    coverImage: "https://images.pexels.com/photos/546819/pexels-photo-546819.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    documents: [
      {
        title: "API Documentation",
        description: "Best practices for documenting APIs",
        href: "/learn/technical-docs/api-docs",
        icon: "code",
        content: `# API Documentation

## Overview

This section provides a high-level summary of the API, including its purpose, core functionalities, and a brief overview of the architecture.

### API Purpose

Clearly articulate what the API is designed to do, the key problems it solves, and mention primary use cases.

### Core Functionalities

List the main features of the API, highlight any unique or advanced functionalities, and provide examples of what can be achieved.

### Architecture Overview

Give a brief overview of the API's architecture, mention any core components or dependencies, and note scalability or performance considerations.`
      },
      {
        title: "Accessibility Guide",
        description: "Guidelines for creating accessible documentation",
        href: "/learn/technical-docs/accessibility",
        icon: "eye",
        content: `# Accessibility Guide

## Accessibility Compliance Checklist

### Design Review

This section ensures all design elements—from color contrast to font size—are considered and optimized to provide a seamless experience for all users, including those with visual impairments.

### Color Contrast

Assess and verify the contrast ratios between text and background colors. Adhere to a minimum contrast ratio of 4.5:1 for normal text and 3:1 for large text to guarantee readability for users, including those with color vision deficiencies.

### Font Size

Standardize a minimum font size of 14 points (18.66 pixels) while maintaining design integrity. Larger font sizes are crucial for users with low vision and help improve the general readability of the content.`
      }
    ]
  },
  {
    id: "planning",
    title: "Product Planning",
    description: "Master the art of product planning with comprehensive guides and templates.",
    coverImage: "https://images.pexels.com/photos/1181671/pexels-photo-1181671.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    documents: [
      {
        title: "OKRs",
        description: "Guide to setting effective OKRs",
        href: "/learn/planning/okrs",
        icon: "target",
        content: `# OKRs

## OKRs Guide

### Objective

Clearly state the main goal you want to achieve. This should be ambitious but achievable. Example: Launch the new AI-driven chatbot feature that boosts user engagement and satisfaction.

### Key Results (One or More Per Objective)

Specify measurable outcomes to track progress towards the objective. Aim for 3-5 key results per objective. Example: Achieve a 10% increase in user engagement as measured by daily active users (DAUs).

### Initiatives (One or More Per Key Result)

Identify the high-level tasks or projects that will help you achieve the key results. Example: Implement natural language processing (NLP) algorithms to enhance AI chatbot responses.`
      },
      {
        title: "Competitive Analysis",
        description: "Framework for analyzing competitors",
        href: "/learn/planning/competitive-analysis",
        icon: "search",
        content: `# Competitive Analysis

## Competitive Analysis Report

### Company Background

Provide a comprehensive understanding of each competitor's foundational aspects. Include relevant history, operational scale, and financial stability to set the context.

### Company Overview

Summarize the competitor's history, company size, and present financial condition. Mention mission statements, vision, core values, and any unique attributes that set them apart.

### Product/Service Overview

Detail the primary products or services offered by the competitor. Discuss key features, unique selling points, and target demographics, along with any notable variations in their offerings.`
      },
      {
        title: "FAQ Document",
        description: "Template for creating effective FAQs",
        href: "/learn/planning/faq",
        icon: "help-circle",
        content: `# FAQ Document

## PR FAQ

### Heading

Name the product in a way the reader (i.e. your target customers) will understand. One sentence under the title.

### Subheading

Describe the customer for the product and what benefits they will gain from using it. One sentence only underneath the Heading.

### Summary Paragraph

Start with the city, media outlet, and your proposed launch date. Give a summary of the product and the benefit.`
      }
    ]
  },
  {
    id: "prototyping",
    title: "Prototyping & Development",
    description: "Learn effective prototyping techniques and development practices.",
    coverImage: "https://images.pexels.com/photos/196644/pexels-photo-196644.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    documents: [
      {
        title: "Prototyping with AI",
        description: "Guide to using AI for rapid prototyping",
        href: "/learn/prototyping/ai-prototyping",
        icon: "cpu",
        content: `# Prototyping with AI

## App Prototyping with AI Code Generation

### Product Description

Provide an overview of the product you're building with key points of interaction and the end goal for product functionality.

### Design and Theme

What design framework (Shadcn, etc...) would you like to use within the project? Any specific color schemes, or support for light vs dark mode?

### Required Development Stack

Outline the application stack you want configured for your product. For example NextJS for full stack (Frontend/API), Vite, Astro, etc...

### Application Backend Requirements

Are there any authentication, database, or other backend configurations you want explicitly created? For example, AuthJS or Clerk for authentication, Supabase or Neon as database tiers? Drizzle or Prisma for ORMs?

### Explicitly Defined Product Flows

Outline the necessary product interactions you expect to happen within your project, for example how would you want your users to experience their first "I Win" moment?

### Explicit Directions for AI Generation

Additional context, description, or parameters you want the generation tool to take into account when building your application.`
      }
    ]
  }
];