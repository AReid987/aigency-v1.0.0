# Survey Automation Framework

An autonomous survey testing framework that continuously validates application stability and reliability by mimicking human user behavior to complete surveys.

## Overview

This framework is built on the Skyvern automation platform and provides:

- **Continuous Operation**: Runs 24/7 without manual intervention
- **Human-like Behavior**: Randomized delays, typing simulation, and realistic interaction patterns
- **Multi-Survey Support**: Adaptable to different survey applications
- **Real-time Monitoring**: Live dashboard with browser view and activity logs
- **Human-in-the-Loop**: Manual override capabilities for debugging

## Architecture

The framework consists of two main components:

1. **Backend Agent** (Python/Skyvern): Core automation engine with scheduling and browser interaction
2. **Frontend Dashboard** (Next.js): Real-time monitoring and control interface

## Quick Start

### Development

```bash
# Install dependencies
pdm install

# Run the backend agent
pdm run dev

# In another terminal, run the frontend dashboard
cd ../dashboard
pnpm dev
```

### Docker

```bash
# Build and run the complete stack
docker-compose up --build
```

## Scripts

- `browser_use_script.py`: Browser automation using browser-use library
- `skyvern_script.py`: Core Skyvern automation script
- `combined_skyvern_script.py`: **Main script** - Combined automation with enhanced features

## Configuration

User profiles and survey data are stored in encrypted configuration files. See `config/` directory for examples.

## Testing

The framework is designed to run continuously for a minimum of 72 hours and supports testing across multiple survey applications simultaneously.

## Documentation

See the `docs/` directory for detailed architecture and implementation documentation.
