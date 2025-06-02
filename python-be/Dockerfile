# Docker multistage build: separate build process and runtime env into different stagees (Excludes redundant build tools and intermediate files to reduces the final image size).

# Stage 1: Build dependencies (Base image).
FROM python:3.13.3-slim AS build

# Prevent Python from writing .pyc files to disc (saves space).
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV POETRY_VERSION=2.1.3

# Set the working directory inside the image.
WORKDIR /app

# Copy only the local files needed for dependency installation into the image.
COPY pyproject.toml poetry.lock ./

# Install dependencies with Poetry (without dev dependencies).
RUN pip install poetry==$POETRY_VERSION \
  && poetry config virtualenvs.create false \
  && poetry install --no-root --without dev \
  && rm -rf /tmp/poetry_cache

# Stage 2: Final runtime image (Base image).
FROM python:3.13.3-slim

# Add a non-root user.
# RUN groupadd appgroup && useradd -m -g appgroup appuser -u 1001
# USER appuser

# Set the working directory inside the image.
WORKDIR /app

# Copy the local Python application code into the image at the WORKDIR.
COPY app/ ./

# Copy pyproject.toml into the runtime stage (Poetry requires the pyproject.toml file to locate and manage dependencies, even at runtime).
COPY pyproject.toml ./

# Copy installed dependencies from the build stage image.
COPY --from=build /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

# EXPOSE 80 # Expose the application port. Not required for Kubernetes pod containers.

# Add a healthcheck.
# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
#   CMD curl --fail http://localhost:80/health || exit 1

# Default command to run when the container starts (How to run the application contained in the image).
CMD ["poetry", "run", "fastapi", "run", "main.py", "--workers", "4", "--port", "80"]

# Consider using a production-grade ASGI server like uvicorn or gunicorn for FastAPI, rather than poetry run fastapi run.
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "4"]
