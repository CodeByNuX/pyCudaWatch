FROM python:3.10-slim

WORKDIR /app

# Install cron
RUN apt-get update && apt-get install -y --no-install-recommends \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app

# Set up cron job: collector runs every minute
RUN echo "* * * * * root python3 /app/collector/collector.py >> /app/collector/cron.log 2>&1" \
    > /etc/cron.d/gpu-collector \
    && chmod 0644 /etc/cron.d/gpu-collector \
    && crontab /etc/cron.d/gpu-collector

# Expose API port
EXPOSE 8000

# Init DB, start cron and API
CMD python3 /app/db/init_db.py && cron && uvicorn api.main:app --host 0.0.0.0 --port 8000

