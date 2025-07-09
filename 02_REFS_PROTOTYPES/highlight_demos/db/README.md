# Knowledge OS Database

This directory contains the database schema, utilities, and migrations for the Knowledge OS system using Drizzle ORM.

## Setup

### 1. Install Dependencies
```bash
pnpm install
```

### 2. Environment Configuration
Copy the example environment file and configure your database:
```bash
cp .env.example .env.local
```

Edit `.env.local` with your database credentials:
```env
DATABASE_URL="postgresql://username:password@localhost:5432/knowledge_os"
```

### 3. Database Setup

#### Option A: Push Schema (Development)
For development, you can push the schema directly:
```bash
npx drizzle-kit push
```

#### Option B: Run Migrations (Production)
For production, use migrations:
```bash
# Generate migrations (already done)
npx drizzle-kit generate

# Run migrations
npx drizzle-kit migrate
```

### 4. Seed Database
Populate the database with sample data:
```bash
pnpm db:seed
```

### 5. Database Studio (Optional)
Open Drizzle Studio to view and edit data:
```bash
npx drizzle-kit studio
```

## Schema Overview

### Core Entities

#### Users
- **users**: User accounts with roles (USER, ADMIN)
- **teams**: Team organizations
- **team_memberships**: User-team relationships with roles

#### Knowledge Management
- **knowledge_bases**: Collections of documents and agents
- **documents**: Text content with metadata and vector IDs
- **chunks**: Document segments for vector search

#### AI Agents
- **agents**: AI agent configurations with capabilities
- **sessions**: User-agent interaction sessions
- **queries**: Individual queries and responses

### Relationships

```
Users ──┐
        ├── Knowledge Bases ── Documents ── Chunks
        ├── Agents ── Sessions ── Queries
        └── Team Memberships ── Teams
```

## Available Scripts

- `pnpm db:generate` - Generate new migrations
- `pnpm db:migrate` - Run pending migrations
- `pnpm db:push` - Push schema changes (dev only)
- `pnpm db:studio` - Open Drizzle Studio
- `pnpm db:seed` - Seed database with sample data

## File Structure

```
db/
├── schema/
│   ├── enums.ts      # PostgreSQL enums
│   └── index.ts      # Main schema definition
├── migrations/       # Generated SQL migrations
├── config.ts         # Database connection
├── types.ts          # TypeScript types
├── utils.ts          # Database utilities
├── seed.ts           # Sample data
└── README.md         # This file
```

## Usage Examples

### Creating a User
```typescript
import { userUtils } from './db/utils';

const user = await userUtils.create({
  name: 'John Doe',
  email: 'john@example.com',
  role: 'USER'
});
```

### Creating a Knowledge Base
```typescript
import { knowledgeBaseUtils } from './db/utils';

const kb = await knowledgeBaseUtils.create({
  name: 'My Knowledge Base',
  description: 'Personal knowledge collection',
  ownerId: user.id
});
```

### Creating an Agent
```typescript
import { agentUtils } from './db/utils';

const agent = await agentUtils.create({
  name: 'AI Assistant',
  type: 'ASSISTANT',
  capabilities: ['Q&A', 'Research'],
  config: { model: 'gpt-4', temperature: 0.7 },
  ownerId: user.id,
  knowledgeBaseId: kb.id
});
```

## Vector Search (Future)

The schema includes `vector_id` fields and `embeddings` arrays for future vector search capabilities. To enable vector search:

1. Install pgvector extension in PostgreSQL
2. Update schema to use vector types
3. Implement similarity search functions

## Troubleshooting

### Connection Issues
- Verify DATABASE_URL is correct
- Ensure PostgreSQL is running
- Check firewall and network settings

### Migration Issues
- Ensure database exists before running migrations
- Check PostgreSQL version compatibility
- Verify user permissions

### Type Issues
- Run `pnpm db:generate` after schema changes
- Restart TypeScript server in your IDE
- Check for circular imports
