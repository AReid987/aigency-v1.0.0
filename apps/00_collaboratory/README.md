# Collaboratory

A modern document collaboration platform built with Next.js, FastAPI, and Supabase.

## Features

- 🔐 User authentication with Supabase Auth
- 📄 Document upload and management
- 💬 Real-time commenting system
- 🤝 Document sharing and collaboration
- 🏷️ AI-powered document tagging
- 📱 Responsive web interface

## Tech Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **Supabase Client** - Authentication and real-time features

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **Supabase** - Backend-as-a-Service (PostgreSQL + Auth)
- **SQLite** - Local development database fallback

## Project Structure

```
collaboratory/
├── apps/
│   ├── api/                 # FastAPI backend
│   │   ├── main.py         # API routes and application
│   │   ├── database.py     # Database models and connection
│   │   ├── supabase_schema.sql  # Database schema for Supabase
│   │   └── ...
│   └── web/                # Next.js frontend
│       ├── app/            # App Router pages
│       ├── components/     # React components
│       └── ...
├── packages/               # Shared packages
└── turbo.json             # Turborepo configuration
```

## Getting Started

### Prerequisites

- Node.js 18+ and pnpm
- Python 3.8+ with pdm
- Supabase account (optional, SQLite fallback available)

### 1. Install Dependencies

```bash
# Install all dependencies
pnpm install

# Install Python dependencies for API
cd apps/api
pdm install
```

### 2. Environment Setup

Create `.env` files in both `apps/api/` and `apps/web/`:

**apps/api/.env:**
```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Database (optional - falls back to SQLite)
DATABASE_URL=postgresql://user:password@host:port/database
```

**apps/web/.env.local:**
```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

### 3. Database Setup

#### Option A: Supabase (Recommended)

1. Create a new Supabase project at [supabase.com](https://supabase.com)
2. Copy your project URL and API keys to the `.env` files
3. Run the SQL schema in Supabase SQL Editor:

```bash
# Copy the contents of apps/api/supabase_schema.sql
# Paste and run in Supabase SQL Editor
```

#### Option B: Local SQLite (Development)

The application will automatically create a local SQLite database if Supabase connection fails.

### 4. Start Development Servers

```bash
# Start both frontend and backend
pnpm dev

# Or start individually:
# Frontend (http://localhost:3003)
cd apps/web && pnpm dev

# Backend (http://localhost:8000)
cd apps/api && pdm run uvicorn main:app --reload
```

### 5. Access the Application

- **Frontend:** http://localhost:3003
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

## Usage

### Authentication

1. Visit http://localhost:3003
2. Sign up with email/password or sign in if you have an account
3. Check your email for confirmation (if using Supabase)

### Document Management

1. Upload documents using the upload form
2. View your documents in the dashboard
3. Share documents with other users
4. Add comments and collaborate

### API Endpoints

- `GET /api/documents` - List user's documents
- `POST /api/documents` - Upload new document
- `GET /api/documents/{id}` - Get document details
- `GET /api/documents/{id}/comments` - Get document comments
- `POST /api/documents/{id}/comments` - Add comment

## Development

### Adding New Features

1. **Backend:** Add routes in `apps/api/main.py`
2. **Frontend:** Create components in `apps/web/app/`
3. **Database:** Update models in `apps/api/database.py`

### Testing

```bash
# Run backend tests
cd apps/api && pdm run pytest

# Run frontend tests
cd apps/web && pnpm test
```

### Building for Production

```bash
# Build all apps
pnpm build

# Build individually
cd apps/web && pnpm build
cd apps/api && pdm build
```

## Deployment

### Frontend (Vercel)

1. Connect your GitHub repo to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push

### Backend (Railway/Heroku)

1. Create new service on Railway/Heroku
2. Connect GitHub repo
3. Set environment variables
4. Deploy

### Database (Supabase)

1. Use Supabase for production database
2. Run the schema from `apps/api/supabase_schema.sql`
3. Configure Row Level Security policies

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details
