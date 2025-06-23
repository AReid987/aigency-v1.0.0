FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    x11vnc \
    fluxbox \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install PDM
RUN pip install pdm

# Set working directory
WORKDIR /workspace

# Copy survey automation app
COPY survey-automation/ ./

# Install dependencies
RUN pdm install

# Install Playwright browsers
RUN pdm run playwright install chromium

# Set up X11 and VNC
ENV DISPLAY=:1
EXPOSE 5901 8000

# Create startup script
RUN echo '#!/bin/bash\n\
echo "Starting X11 and VNC..."\n\
Xvfb :1 -screen 0 1024x768x24 &\n\
sleep 2\n\
x11vnc -display :1 -nopw -listen 0.0.0.0 -xkb -ncache 10 -ncache_cr -forever &\n\
fluxbox -display :1 &\n\
echo "X11 and VNC started on port 5901"\n\
echo "Starting survey automation backend..."\n\
exec "$@"' > /usr/local/bin/start-services.sh && chmod +x /usr/local/bin/start-services.sh

ENTRYPOINT ["/usr/local/bin/start-services.sh"]
CMD ["pdm", "run", "dev"]
