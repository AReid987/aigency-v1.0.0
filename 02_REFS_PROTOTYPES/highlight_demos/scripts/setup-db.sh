#!/bin/bash

# Knowledge OS Database Setup Script

echo "🚀 Setting up Knowledge OS Database..."

# Check if PostgreSQL is running
if ! pg_isready -q; then
    echo "❌ PostgreSQL is not running. Please start PostgreSQL first."
    echo "   macOS: brew services start postgresql"
    echo "   Ubuntu: sudo systemctl start postgresql"
    echo "   Docker: docker run --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres"
    exit 1
fi

echo "✅ PostgreSQL is running"

# Create database if it doesn't exist
DB_NAME="knowledge_os"
DB_USER="postgres"
DB_PASSWORD="password"

echo "📦 Creating database '$DB_NAME'..."

# Try to create database (will fail silently if exists)
createdb -U $DB_USER $DB_NAME 2>/dev/null || echo "Database '$DB_NAME' already exists"

# Install pgvector extension
echo "🔧 Installing pgvector extension..."
psql -U $DB_USER -d $DB_NAME -c "CREATE EXTENSION IF NOT EXISTS vector;" 2>/dev/null || echo "pgvector extension not available (optional)"

echo "✅ Database setup complete!"

# Run migrations
echo "📋 Running database migrations..."
npx drizzle-kit push

echo "🌱 Seeding database with sample data..."
pnpm db:seed

echo "🎉 Database setup completed successfully!"
echo ""
echo "📊 Next steps:"
echo "   1. Start the development server: pnpm dev"
echo "   2. Open Drizzle Studio: npx drizzle-kit studio"
echo "   3. View the application: http://localhost:3000"
