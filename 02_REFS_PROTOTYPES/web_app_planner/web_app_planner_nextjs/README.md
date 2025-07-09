This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Supabase Project Setup

To integrate Supabase with this project, follow these steps:

1.  **Create a New Supabase Project:**

    - Go to the [Supabase website](https://supabase.com/) and sign in.
    - Click "New Project" and follow the prompts to create a new project. Choose a strong password for your database.

2.  **Obtain API Keys:**

    - Once your project is created, navigate to "Project Settings" (the gear icon) > "API".
    - Locate your "Project URL" and "Project API keys" (specifically the `anon` public key).

3.  **Configure Environment Variables:**

    - Create a file named `.env.local` in the root of this `web_app_planner_nextjs` directory.
    - Add the following variables to `.env.local`, replacing the placeholders with your actual keys:

      ```
      NEXT_PUBLIC_SUPABASE_URL=YOUR_SUPABASE_URL
      NEXT_PUBLIC_SUPABASE_ANON_KEY=YOUR_SUPABASE_ANON_KEY
      ```

    - These variables will be accessible in your Next.js application. Remember to restart your development server if you change these values.

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
