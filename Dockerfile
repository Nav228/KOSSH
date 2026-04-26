FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PORT=5002
# Performance optimizations
ENV PYTHONOPTIMIZE=2
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    mdbtools \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create logs directory
RUN mkdir -p /app/logs

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port (Koyeb/Railway/Render inject their own $PORT at runtime)
EXPOSE 5002

# Run the application with Gunicorn — bind to $PORT so it works locally and on cloud
CMD gunicorn --bind 0.0.0.0:${PORT:-5002} --workers 2 --threads 2 --worker-class gthread --timeout 120 --keep-alive 5 --access-logfile - --error-logfile - app:app