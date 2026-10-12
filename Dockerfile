# ==========================================
# LMS01 FX Learning Agent - Monolithic Container
# Serves both Web Studio UI and REST API on Port 8080
# ==========================================
FROM python:3.11-slim

WORKDIR /app

# Install curl and git for scraper dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python backend dependencies
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY backend /app/backend
COPY course_research /app/course_research
COPY web_preview /app/web_preview

# Ensure output directory exists for runtime generated packages
RUN mkdir -p /app/output

# Set Python module path
ENV PYTHONPATH=/app
ENV PORT=8080

EXPOSE 8080

# Single entrypoint: FastAPI serves UI at '/' and API at '/api/*'
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8080"]
