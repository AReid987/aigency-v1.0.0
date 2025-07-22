# Survey Automation Framework Setup Guide

This guide will help you set up the Daytona sandbox and test your survey automation framework.

## Prerequisites

- Docker and Docker Compose installed
- Daytona CLI installed
- Access to your Agent Zero container with the survey scripts

## Step 1: Copy Scripts from Agent Zero Container

First, you need to copy your existing scripts from the Agent Zero container:

```bash
# Find your Agent Zero container
docker ps

# Copy the scripts (replace 'agent-zero-container' with your actual container name/id)
./copy-agent-zero-scripts.sh agent-zero-container
```

This will copy:
- `/root/browser_use_script.py` → `apps/survey-automation/scripts/browser_use_script.py`
- `/root/skyvern_script.py` → `apps/survey-automation/scripts/skyvern_script.py`
- `/root/combined_skyvern_script.py` → `apps/survey-automation/scripts/combined_skyvern_script.py`

## Step 2: Set Up Daytona Sandbox

Create and start a Daytona workspace:

```bash
# Create the workspace
daytona create --config .daytona/config.yaml

# Or if you prefer to use the existing directory
daytona create . --name aigency-survey-automation
```

## Step 3: Local Development (Alternative)

If you prefer to test locally without Daytona:

### Option A: Using Docker Compose
```bash
# Start the complete stack with Docker
pnpm run dev:survey-docker
```

This will:
- Build and start the survey automation backend on port 8000
- Start a VNC server on port 8080 for browser viewing
- Set up the necessary networking

### Option B: Direct Python Development
```bash
# Navigate to the survey automation app
cd apps/survey-automation

# Install dependencies
pdm install

# Start the backend
pdm run dev
```

## Step 4: Integration with Combined Script

Once your scripts are copied, you'll need to integrate the `combined_skyvern_script.py` with the framework:

1. **Update `app/agent.py`**: Replace the placeholder logic in `start_survey_task()` with calls to your combined script
2. **Configure profiles**: Set up user profiles and survey configurations in the `config/` directory
3. **Test the scheduler**: Verify that the APScheduler can trigger your survey automation

## Step 5: Testing the Framework

### Backend API Testing
```bash
# Check if the backend is running
curl http://localhost:8000/

# Get agent status
curl http://localhost:8000/api/status

# Pause the agent
curl -X POST http://localhost:8000/api/agent/pause

# Resume the agent
curl -X POST http://localhost:8000/api/agent/resume
```

### Browser Viewing
- Open http://localhost:8080 in your browser to see the VNC view of the automated browser

## Step 6: Next Steps

After basic testing works:

1. **Create Frontend Dashboard**: Build a Next.js app for real-time monitoring
2. **Implement WebSocket Communication**: For live updates between backend and frontend
3. **Add Configuration Management**: Secure storage for user profiles and survey data
4. **Enhance Error Handling**: Robust error recovery and logging
5. **Add Anti-Detection Features**: Implement human-like behavior patterns

## Project Structure

```
apps/survey-automation/
├── app/                    # Main application code
│   ├── main.py            # FastAPI entry point
│   ├── agent.py           # Core automation logic
│   ├── scheduler.py       # APScheduler integration
│   └── api.py             # REST API endpoints
├── scripts/               # Your Agent Zero scripts
│   ├── browser_use_script.py
│   ├── skyvern_script.py
│   └── combined_skyvern_script.py  # Main script
├── config/                # Configuration files
├── tests/                 # Test files
├── Dockerfile            # Container configuration
└── pyproject.toml        # Python dependencies
```

## Troubleshooting

### Common Issues

1. **Chrome/Browser Issues**: Make sure Xvfb is running and DISPLAY is set correctly
2. **Permission Issues**: Ensure Docker has proper permissions for volume mounts
3. **Port Conflicts**: Check if ports 8000 and 8080 are available

### Logs

Check application logs:
```bash
# Docker logs
docker-compose -f docker-compose.survey.yml logs -f

# Direct Python logs
cd apps/survey-automation && pdm run dev
```

## Architecture Overview

The framework follows the architecture documented in your Aigency Agile Squad docs:

- **Backend Agent**: Python/Skyvern for automation
- **Scheduler**: APScheduler for continuous operation
- **API Layer**: FastAPI for control and monitoring
- **Browser Control**: Headless Chrome with VNC for viewing
- **Future Frontend**: Next.js dashboard for real-time monitoring

This setup provides a solid foundation for testing your survey automation framework in a controlled environment before scaling to production use.
