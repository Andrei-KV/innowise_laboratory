# Base image
FROM python:3.12-slim

# Install poetry
RUN pip install poetry

# Install system dependences
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Like "cd /app"
WORKDIR /app

# Copy dependencies files
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry
# This single RUN command executes several steps:
# 1. Configures Poetry not to create a separate virtual environment inside the container.
#    Since the container itself is an isolated environment, virtualenvs are redundant.
# 2. Installs only 'main' dependencies (skips 'dev' dependencies) to minimize the image size.
# 3. Instructs Poetry not to install the root project itself, as the code is already copied.
# 4. Ensures the command runs without expecting any user interaction.
RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-root --no-interaction

# Copy in the source code
COPY main.py .
COPY README.md .
COPY database.py .
COPY models.py .
COPY schemas.py .

EXPOSE 8000

# Setup an app user so the container doesn't run as the root user
# Rules for user to add files
RUN useradd -m app && chown -R app:app /app
USER app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
