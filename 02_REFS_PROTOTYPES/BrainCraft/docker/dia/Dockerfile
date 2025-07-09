FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gnupg ca-certificates && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3B4FE6ACC0B21F32 871920D1991BC93C && \
    apt-get update && apt-get install -y --no-install-recommends \
    git \
    ffmpeg \
    libsndfile1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install Dia from GitHub repository
RUN pip install --no-cache-dir git+https://github.com/nari-labs/dia.git

# Install FastAPI and Uvicorn for the API server
RUN pip install --no-cache-dir fastapi uvicorn pydantic

# Copy the API server code
COPY api_server.py /app/

# Expose port 5002
EXPOSE 5002

# Download model on startup
ENV TRANSFORMERS_CACHE=/app/models
ENV HF_HOME=/app/models

# Set up entrypoint to run the API server
CMD ["python", "api_server.py"]