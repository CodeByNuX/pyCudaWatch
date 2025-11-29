FROM nvidia/cuda:12.3.0-runtime-ubuntu22.04

WORKDIR /app

# Install Python + cron
RUN apt-get update && apt-get install -y \
    python3 python3-pip cron && \
    rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy entire application code
COPY . /app

# Create cron job (NO “root” field)
RUN echo "* * * * * /usr/bin/python3 /app/collector/collector.py >> /app/collector/cron.log 2>&1" \
    > /etc/cron.d/gpu-collector \
    && chmod 0644 /etc/cron.d/gpu-collector \
    && crontab /etc/cron.d/gpu-collector

EXPOSE 8000

# Startup: init DB → start cron → start API
CMD python3 /app/db/init_db.py && cron && uvicorn api.main:app --host 0.0.0.0 --port 8000
