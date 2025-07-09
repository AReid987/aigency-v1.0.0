<div align="center">
  <img src="assets/braincraft-logo.png" alt="BrainCraft Logo" width="200"/>

# BrainCraft

🧠 Your Personal Brainstorming & Diagramming AI Agent

[![License: MIT](https://img.shields.io/badge/License-BSD-yellow.svg)](https://opensource.org/licenses/BSD)
[![Node.js Version](https://img.shields.io/badge/node-%3E%3D16-brightgreen)](https://nodejs.org)
[![Python Version](https://img.shields.io/badge/python-%3E%3D3.10-blue)](https://www.python.org)
[![Docker](https://img.shields.io/badge/docker-supported-blue)](https://www.docker.com)

Transform your ideas into visual diagrams through natural conversation - both text and voice! 🎯

</div>

## 🌟 Features

- 🤖 **AI-Powered Brainstorming** - Collaborate with an intelligent AI agent to explore and refine your ideas
- 🗣️ **Voice Interaction** - Hands-free brainstorming with voice commands and AI vocal responses
- 📊 **Real-time Diagramming** - Watch your ideas transform into diagrams as you speak or type
- 🔄 **Interactive Refinement** - Instantly update diagrams through natural conversation
- 📝 **Multiple Diagram Types** - Support for flowcharts, sequence diagrams, class diagrams, and more
- 🎨 **Modern UI/UX** - Sleek, intuitive interface with customizable themes
- ⚡ **Real-time Updates** - See your diagrams evolve instantly as you brainstorm

## 🎬 Demo

Watch BrainCraft in action:

![BrainCraft Demo](assets/demo.gif)

## 🚀 Getting Started

### Prerequisites

- Node.js (v16 or higher)
- Python (3.10 or higher)
- npm or yarn package manager
- Docker and Docker Compose (for containerized setup)

### 🐳 Option 1: Docker Setup (Recommended)

1. Configure environment files:

```bash
# Set up backend environment
cp backend/.env.example backend/.env
# Edit backend/.env and add your API keys:
# - Choose your LLM provider by setting LLM_PROVIDER (mistral, gemini, or openrouter)
# - Add the corresponding API key (MISTRAL_API_KEY, GEMINI_API_KEY, or OPENROUTER_API_KEY)
# - OPENAI_API_KEY (required for voice transcription)
# - Configure Nari Labs Dia settings for text-to-speech

# Set up frontend environment
cp frontend/.env.local.example frontend/.env.local
```

2. Launch with Docker Compose:

```bash
docker compose -f docker/docker-compose.yml up
```

🌐 Access the application:

- Web Interface: http://localhost:3000
- API Endpoint: http://localhost:8000

To stop:

```bash
docker compose -f docker/docker-compose.yml down
```

### 💻 Option 2: Local Setup

#### Frontend Setup

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

#### Backend Setup

```bash
cd backend
uv sync
cp .env.example .env
# Configure API keys in .env:
# - LLM_PROVIDER: Choose between mistral, gemini, or openrouter
# - Add corresponding API key (MISTRAL_API_KEY, GEMINI_API_KEY, or OPENROUTER_API_KEY)
# - OPENAI_API_KEY: For voice transcription
# - Configure Nari Labs Dia settings for text-to-speech

uv run uvicorn src.main:app --reload --port 8000
```

## 🎯 Usage

1. 🌐 Open BrainCraft in your browser at `http://localhost:3000`
2. 🎤 Choose between voice or text input mode
3. 🗣️ Start brainstorming! Describe your ideas naturally
4. 📊 Watch as your thoughts transform into professional diagrams
5. 🔄 Refine the diagrams through conversation
6. 🎨 Customize the appearance to match your preferences

## 🛠️ Technology Stack

- **Frontend**: Next.js, TypeScript, Mermaid.js for diagramming
- **Backend**: FastAPI, multiple LLM providers ([Mistral AI](https://mistral.ai/), [Google Gemini](https://ai.google.dev/), [OpenRouter](https://openrouter.ai/)), [Nari Labs Dia](https://github.com/nari-labs/dia) for ultra-realistic speech synthesis, [OpenAI](https://openai.com/) Whisper for voice transcription and [Langchain](https://www.langchain.com/) for agentic workflow
- **Containerization**: Docker & Docker Compose

## 🏆 Hackathon Submission

<div align="center">
  <a href="https://techberlin.io/">
    <img src="assets/code-berlin-hackathon-banner.png" alt="Tech: Berlin Hackathon Banner" width="400"/>
  </a>
</div>

This project was created as part of the **Tech: Berlin** hackathon. We aimed to revolutionize the way people brainstorm and visualize their ideas by combining the power of AI, voice interaction, and real-time diagramming. Our solution enables a more natural and intuitive way to create and refine diagrams, making the brainstorming process more efficient and enjoyable.

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

BrainCraft is open-source software licensed under the BSD-3-Clause License. See the [LICENSE](LICENSE) file for details.

---

Made with ❤️ by [ScrapegraphAI](https://scrapegraphai.com)
