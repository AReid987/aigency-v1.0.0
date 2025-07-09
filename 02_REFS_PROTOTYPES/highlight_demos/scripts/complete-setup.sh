#!/bin/bash

# Knowledge OS Complete Setup Script
# This script sets up the entire Knowledge OS system

echo "🚀 Knowledge OS Complete Setup"
echo "==============================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check prerequisites
echo "🔍 Checking prerequisites..."

# Check Node.js
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    print_error "Node.js version 18+ is required. Current version: $(node -v)"
    exit 1
fi
print_status "Node.js $(node -v) is installed"

# Check pnpm
if ! command -v pnpm &> /dev/null; then
    print_warning "pnpm is not installed. Installing pnpm..."
    npm install -g pnpm
fi
print_status "pnpm $(pnpm -v) is available"

# Check PostgreSQL
if ! command -v psql &> /dev/null; then
    print_warning "PostgreSQL is not installed or not in PATH"
    print_info "Please install PostgreSQL:"
    print_info "  macOS: brew install postgresql"
    print_info "  Ubuntu: sudo apt-get install postgresql postgresql-contrib"
    print_info "  Or use Docker: docker run --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    print_status "PostgreSQL is installed"
fi

# Check Python (for FastAPI backend)
if ! command -v python3 &> /dev/null; then
    print_warning "Python 3 is not installed"
    print_info "Please install Python 3.8+ for the FastAPI backend"
else
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_status "Python $PYTHON_VERSION is installed"
fi

echo ""
echo "📦 Installing dependencies..."

# Install Node.js dependencies
print_info "Installing Node.js dependencies..."
pnpm install

if [ $? -ne 0 ]; then
    print_error "Failed to install Node.js dependencies"
    exit 1
fi
print_status "Node.js dependencies installed"

# Install Python dependencies (if requirements.txt exists)
if [ -f "requirements.txt" ]; then
    print_info "Installing Python dependencies..."
    if command -v pip3 &> /dev/null; then
        pip3 install -r requirements.txt
        print_status "Python dependencies installed"
    else
        print_warning "pip3 not found, skipping Python dependencies"
    fi
fi

echo ""
echo "🗄️  Setting up database..."

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    print_info "Creating .env.local file..."
    cp .env.example .env.local
    print_status ".env.local created from template"
    print_warning "Please update DATABASE_URL in .env.local with your PostgreSQL credentials"
else
    print_status ".env.local already exists"
fi

# Database setup
print_info "Setting up PostgreSQL database..."

# Try to create database
DB_NAME="knowledge_os"
DB_USER="postgres"

# Check if database exists
if command -v psql &> /dev/null; then
    if psql -U $DB_USER -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
        print_status "Database '$DB_NAME' already exists"
    else
        print_info "Creating database '$DB_NAME'..."
        createdb -U $DB_USER $DB_NAME 2>/dev/null
        if [ $? -eq 0 ]; then
            print_status "Database '$DB_NAME' created"
        else
            print_warning "Could not create database. Please create it manually:"
            print_info "  createdb -U postgres knowledge_os"
        fi
    fi

    # Try to install pgvector extension
    print_info "Installing pgvector extension..."
    psql -U $DB_USER -d $DB_NAME -c "CREATE EXTENSION IF NOT EXISTS vector;" 2>/dev/null
    if [ $? -eq 0 ]; then
        print_status "pgvector extension installed"
    else
        print_warning "pgvector extension not available (optional for vector search)"
    fi
else
    print_warning "PostgreSQL not accessible, skipping database creation"
fi

echo ""
echo "🔄 Running database migrations..."

# Generate and run migrations
print_info "Generating database schema..."
npx drizzle-kit generate

if [ $? -eq 0 ]; then
    print_status "Database schema generated"
else
    print_error "Failed to generate database schema"
    exit 1
fi

print_info "Pushing schema to database..."
npx drizzle-kit push

if [ $? -eq 0 ]; then
    print_status "Database schema pushed"
else
    print_warning "Failed to push schema. You may need to configure DATABASE_URL in .env.local"
fi

echo ""
echo "🌱 Seeding database..."

# Seed database
print_info "Seeding database with sample data..."
pnpm db:seed

if [ $? -eq 0 ]; then
    print_status "Database seeded with sample data"
else
    print_warning "Failed to seed database. You can run 'pnpm db:seed' manually later"
fi

echo ""
echo "🔧 Building application..."

# Build the application
print_info "Building Next.js application..."
pnpm build

if [ $? -eq 0 ]; then
    print_status "Application built successfully"
else
    print_error "Failed to build application"
    exit 1
fi

echo ""
echo "🎉 Setup Complete!"
echo "=================="
print_status "Knowledge OS is ready to use!"

echo ""
echo "📋 Next Steps:"
echo "1. Start the development server:"
echo "   pnpm dev"
echo ""
echo "2. Open your browser to:"
echo "   http://localhost:3000"
echo ""
echo "3. (Optional) Start the FastAPI backend:"
echo "   cd api && python3 main.py"
echo ""
echo "4. (Optional) Open Drizzle Studio:"
echo "   npx drizzle-kit studio"
echo ""

print_info "Available scripts:"
echo "  pnpm dev          - Start development server"
echo "  pnpm build        - Build for production"
echo "  pnpm db:studio    - Open database studio"
echo "  pnpm db:seed      - Seed database with sample data"
echo "  pnpm db:generate  - Generate new migrations"
echo "  pnpm db:push      - Push schema changes to database"

echo ""
print_warning "Don't forget to:"
echo "1. Update .env.local with your actual database credentials"
echo "2. Configure OAuth providers (Google, GitHub) if needed"
echo "3. Set up your AI API keys (OpenAI, Anthropic) for agent functionality"

echo ""
print_status "Happy coding! 🚀"
