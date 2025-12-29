FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system deps (minimal)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install Poetry
RUN pip install --no-cache-dir poetry

# Disable venv creation (use container env)
RUN poetry config virtualenvs.create false

# Install Python dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# Copy application code
COPY aletheia ./aletheia
COPY data ./data
COPY checkpoints ./checkpoints

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "aletheia.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
