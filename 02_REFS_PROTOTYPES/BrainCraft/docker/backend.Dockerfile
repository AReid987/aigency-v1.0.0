FROM python:3.12-slim

WORKDIR /app/backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install PDM
RUN pip install --no-cache-dir pdm

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# Copy backend files first
COPY backend/pyproject.toml backend/pdm.lock ./
COPY backend/src/ ./src/

# Install dependencies using PDM
RUN pdm install --no-self --no-editable

# Copy config files
COPY backend/.env ./.env

ENV PATH="/app/backend/__pypackages__/3.12/bin:$PATH" \
    PYTHONPATH="/app/backend/__pypackages__/3.12/lib"

# Set Python environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["pdm", "run", "uvicorn", "src.combined_main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
