# AIgency Turborepo

This Turborepo contains a mix of JavaScript/TypeScript and Python applications.

## What's inside?

This Turborepo includes the following packages/apps:

### Apps and Packages

- `docs`: a [Next.js](https://nextjs.org/) app
- `web`: another [Next.js](https://nextjs.org/) app
- `extract`: a Python app for extracting insights from YouTube videos and articles
- `@repo/ui`: a stub React component library shared by both `web` and `docs` applications
- `@repo/eslint-config`: `eslint` configurations (includes `eslint-config-next` and `eslint-config-prettier`)
- `@repo/typescript-config`: `tsconfig.json`s used throughout the monorepo

The JavaScript/TypeScript apps and packages are 100% [TypeScript](https://www.typescriptlang.org/), while the `extract` app is built with Python and PDM.

### Utilities

This Turborepo has some additional tools already setup for you:

- [TypeScript](https://www.typescriptlang.org/) for static type checking
- [ESLint](https://eslint.org/) for code linting
- [Prettier](https://prettier.io) for code formatting
- [PDM](https://pdm.fming.dev/) for Python dependency management

### Build

To build all apps and packages, run the following command:

```
cd my-turborepo
pnpm build
```

### Develop

To develop all apps and packages (including the Python extract app), run the following command:

```
cd my-turborepo
pnpm dev
```

To develop only JavaScript/TypeScript apps (excluding the Python extract app):

```
cd my-turborepo
pnpm dev:js
```

To develop only the Python extract app:

```
cd my-turborepo
pnpm dev:extract
```

### Python App Development

The `extract` app is a Python application managed with PDM. To work with it directly:

```bash
# Navigate to the extract app directory
cd apps/extract

# Install dependencies
pdm install

# Run the app
pdm run dev

# Run tests
pdm run test

# Run linting
pdm run lint
```

See the [extract app README](./apps/extract/README.md) for more details.

## Roadmap

The following features are planned for future development:

1. **MCP Support for @aigency/extract**: Implement Model Context Protocol support for the extract app to enable enhanced AI capabilities and tool integration
2. **Unified Authentication**: Single sign-on across all apps in the monorepo
3. **Shared Data Layer**: Common data access layer between JavaScript and Python apps
4. **Enhanced CI/CD Pipeline**: Automated testing and deployment for both JS and Python apps
5. **Documentation Site**: Comprehensive documentation for all apps and packages
6. **Performance Optimization**: Improve build and runtime performance
7. **Cross-App Communication**: Enable real-time communication between apps

### Remote Caching

> [!TIP]
> Vercel Remote Cache is free for all plans. Get started today at [vercel.com](https://vercel.com/signup?/signup?utm_source=remote-cache-sdk&utm_campaign=free_remote_cache).

Turborepo can use a technique known as [Remote Caching](https://turborepo.com/docs/core-concepts/remote-caching) to share cache artifacts across machines, enabling you to share build caches with your team and CI/CD pipelines.

By default, Turborepo will cache locally. To enable Remote Caching you will need an account with Vercel. If you don't have an account you can [create one](https://vercel.com/signup?utm_source=turborepo-examples), then enter the following commands:

```
cd my-turborepo
npx turbo login
```

This will authenticate the Turborepo CLI with your [Vercel account](https://vercel.com/docs/concepts/personal-accounts/overview).

Next, you can link your Turborepo to your Remote Cache by running the following command from the root of your Turborepo:

```
npx turbo link
```

## Useful Links

Learn more about the power of Turborepo:

- [Tasks](https://turborepo.com/docs/crafting-your-repository/running-tasks)
- [Caching](https://turborepo.com/docs/crafting-your-repository/caching)
- [Remote Caching](https://turborepo.com/docs/core-concepts/remote-caching)
- [Filtering](https://turborepo.com/docs/crafting-your-repository/running-tasks#using-filters)
- [Configuration Options](https://turborepo.com/docs/reference/configuration)
- [CLI Usage](https://turborepo.com/docs/reference/command-line-reference)
