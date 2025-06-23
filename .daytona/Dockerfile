FROM ubuntu:22.04

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    python3 \
    python3-pip \
    python3-venv \
    nodejs \
    npm \
    xvfb \
    x11vnc \
    fluxbox \
    wget \
    gnupg \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install PDM
RUN pip3 install pdm

# Install pnpm
RUN npm install -g pnpm

# Set up workspace
WORKDIR /workspace

# Copy project files
COPY . .

# Install Node.js dependencies
RUN pnpm install

# Install Python dependencies for survey automation
WORKDIR /workspace/apps/survey-automation
RUN pdm install

# Install Playwright browsers
RUN pdm run playwright install chromium

# Set up X11 and VNC
ENV DISPLAY=:1
EXPOSE 5901 8000 3000

# Create startup script
RUN echo '#!/bin/bash\n\
Xvfb :1 -screen 0 1024x768x24 &\n\
x11vnc -display :1 -nopw -listen localhost -xkb -ncache 10 -ncache_cr -forever &\n\
fluxbox -display :1 &\n\
exec "$@"' > /usr/local/bin/start-x11.sh && chmod +x /usr/local/bin/start-x11.sh

ENTRYPOINT ["/usr/local/bin/start-x11.sh"]
CMD ["bash"]
