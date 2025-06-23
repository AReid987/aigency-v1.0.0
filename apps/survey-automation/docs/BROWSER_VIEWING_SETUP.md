# Browser Viewing Setup Guide

## ✅ Completed Setup

### 1. Scripts Successfully Copied
- ✅ `browser_use_script.py` - Browser automation using browser-use library
- ✅ `skyvern_script.py` - Core Skyvern automation script  
- ✅ `combined_skyvern_script.py` - **Main script** with enhanced features

### 2. Framework Structure Created
- ✅ FastAPI backend with REST API and WebSocket support
- ✅ APScheduler for continuous 24/7 operation
- ✅ Enhanced agent with browser viewing capabilities
- ✅ Docker configuration for containerized deployment

## 🎯 Browser Viewing Options

### Option 1: Stagehand (BrowserBase) - **RECOMMENDED**

**Why it's the best choice:**
- Built-in live browser viewing via WebSocket streaming
- AI-powered automation that can complement your existing scripts
- Professional anti-detection features
- Automatic session recording
- Cloud-based infrastructure (no local browser management)

**Setup:**
```bash
# 1. Sign up for BrowserBase account
# Visit: https://browserbase.com

# 2. Get API credentials
export BROWSERBASE_API_KEY="your-api-key"
export BROWSERBASE_PROJECT_ID="your-project-id"

# 3. Install Stagehand
cd apps/survey-automation
npm install @browserbase/stagehand

# 4. Test integration
pdm run dev
# Then visit: http://localhost:8000/api/live-view
```

**Integration Status:**
- ✅ Python wrapper created (`stagehand_integration.py`)
- ✅ Enhanced agent with viewing capabilities
- ✅ API endpoints for live view URL
- 🔄 Requires BrowserBase API key to activate

### Option 2: X11 Forwarding + VNC - **CURRENT FALLBACK**

**Setup:**
```bash
# Start with VNC viewing
pnpm run dev:survey-docker

# Access browser view at:
# http://localhost:8080 (VNC web interface)
```

**Pros:** Free, works with any automation tool
**Cons:** Requires VNC client, can be laggy

### Option 3: OpenOperator - **OPEN SOURCE ALTERNATIVE**

```bash
# Install OpenOperator
pip install openoperator

# Integration example:
from openoperator import OpenOperator
operator = OpenOperator(enable_recording=True)
```

### Option 4: Other Options Analysis

| Tool | Status | Best For | Cost |
|------|--------|----------|------|
| **Stagehand** | ✅ Integrated | Production use, AI automation | Paid |
| **X11/VNC** | ✅ Available | Development, debugging | Free |
| **OpenOperator** | 🔄 Experimental | Open source projects | Free |
| **Blast AI** | 🔄 Research | Enterprise automation | Paid |
| **Suna** | 🔄 Research | Lightweight automation | Unknown |
| **AgentSeek** | 🔄 Research | Agent-specific tasks | Unknown |
| **Agent S** | 🔄 Research | Academic research | Free |

## 🚀 Quick Start Testing

### 1. Test the Framework
```bash
cd apps/survey-automation

# Start the backend
pdm run dev

# In another terminal, run tests
python test_framework.py
```

### 2. Test API Endpoints
```bash
# Check status
curl http://localhost:8000/api/status

# Get browser options
curl http://localhost:8000/api/browser-options

# Start a test survey
curl -X POST http://localhost:8000/api/survey/start \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Survey",
    "url": "https://example.com/survey",
    "profile": "default",
    "enable_viewing": true
  }'
```

### 3. View Live Browser (when Stagehand is configured)
```bash
# Get live view URL
curl http://localhost:8000/api/live-view

# Response will include:
# {
#   "available": true,
#   "url": "https://browserbase.com/sessions/live/your-session-id",
#   "status": "active"
# }
```

## 🔧 Integration with Your Scripts

Your existing scripts are now integrated as follows:

1. **`combined_skyvern_script.py`** → Main automation logic
2. **Enhanced Agent** → Wraps your scripts with viewing capabilities
3. **Stagehand Integration** → Provides live browser viewing
4. **API Layer** → Exposes control and monitoring endpoints

## 🎛️ Dashboard Development (Next Phase)

Create a Next.js dashboard to embed the live browser view:

```bash
# Create dashboard app
cd apps
npx create-next-app@latest dashboard --typescript --tailwind --app

# Add Stagehand live view component
# This will embed the browser view directly in your dashboard
```

## 🐳 Daytona Sandbox (Alternative Approach)

Since Daytona had file size issues, alternative approaches:

### Option A: Use GitHub Codespaces
```bash
# Create .devcontainer/devcontainer.json
# Push to GitHub and open in Codespaces
```

### Option B: Use Docker Compose Locally
```bash
# Already configured
pnpm run dev:survey-docker
```

### Option C: Manual Daytona Setup
```bash
# Create minimal Dockerfile and try again
daytona sandbox create --dockerfile .daytona/minimal/Dockerfile
```

## 🔐 Environment Variables

Create `.env` file:
```bash
# BrowserBase (for Stagehand)
BROWSERBASE_API_KEY=your-api-key
BROWSERBASE_PROJECT_ID=your-project-id

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true

# Browser Configuration
HEADLESS=false
BROWSER_WIDTH=1024
BROWSER_HEIGHT=768

# Scheduler
SCHEDULER_INTERVAL_HOURS=4
SCHEDULER_ENABLED=true
```

## 📊 Monitoring and Debugging

### Real-time Monitoring
- **Live View**: Browser automation in real-time
- **API Status**: Current agent status and statistics
- **Logs**: Detailed execution logs
- **Screenshots**: Automatic screenshot capture
- **Session Recordings**: Full session playback

### Debug Mode
```bash
# Enable debug logging
export DEBUG=true
pdm run dev
```

## 🎯 Next Steps Priority

1. **High Priority**: Set up BrowserBase account for Stagehand integration
2. **Medium Priority**: Create Next.js dashboard with embedded live view
3. **Low Priority**: Explore alternative viewing options (OpenOperator, etc.)

The framework is now ready for testing with browser viewing capabilities!
