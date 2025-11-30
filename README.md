# pyCudaWatch

pyCudaWatch is a lightweight GPU monitoring dashboard that runs entirely
inside Docker. It collects NVIDIA GPU metrics (utilization, memory
usage, temperature) using NVML and displays them in a web-based
dashboard built with FastAPI and Chart.js. All data is stored in SQLite,
and the container automatically performs cleanup and maintenance.

------------------------------------------------------------------------

## Features

-   Runs 100% inside Docker (no host Python required)
-   Automatic GPU metric collection using NVIDIA NVML
-   Collector executes every minute using cron inside the container
-   FastAPI dashboard with Bootstrap dark mode and Chart.js
    visualizations
-   SQLite database for persistent storage
-   Automatic hourly cleanup:
    -   Purges data older than 30 days
    -   Performs safe VACUUM outside transaction
-   Works with any NVIDIA GPU visible to NVML
-   GPU passthrough using NVIDIA Container Toolkit

------------------------------------------------------------------------

## Requirements

Before running pyCudaWatch, your host system must have:

1.  An NVIDIA GPU with drivers installed.

2.  NVIDIA Container Toolkit:

    ``` bash
    sudo apt install nvidia-container-toolkit
    sudo systemctl restart docker
    ```

Verify Docker can access your GPU:

``` bash
docker run --rm --gpus all nvidia/cuda:12.3.0-runtime-ubuntu22.04 nvidia-smi
```

If your GPU information appears, Docker GPU passthrough is working.

------------------------------------------------------------------------

## Project Structure

    pyCudaWatch/
    ├── api/                 # FastAPI routes and dashboard logic
    ├── collector/           # GPU collector and cron logs
    ├── dashboard/           # HTML templates and JavaScript
    ├── db/                  # SQLite DB and initialization script
    ├── Dockerfile
    └── docker-compose.yml

------------------------------------------------------------------------

## Running pyCudaWatch (Docker Only)

### 1. Build the container

Use `--no-cache` after making code changes:

``` bash
docker compose build --no-cache
```

### 2. Start the application

``` bash
docker compose up -d
```

### 3. View container logs (optional)

``` bash
docker logs -f pycudawatch
```

------------------------------------------------------------------------

## Accessing the Dashboard

Open your browser and visit:

    http://localhost:8000

The dashboard displays:

-   GPU utilization (percent)
-   Memory used
-   Temperature (°C)
-   Utilization over time
-   Temperature over time

The dashboard auto-refreshes every 30 seconds.

------------------------------------------------------------------------

## Data Persistence

The SQLite database lives on the host in:

    ./db/gpu_stats.db

This file is bind-mounted from the container, so your historical data
remains intact even after recreating or updating the container.

------------------------------------------------------------------------

## Automatic Cleanup and Maintenance

The collector runs once per minute using cron inside the container.

At the start of every hour (`minute == 0`):

1.  The collector deletes rows older than 30 days.
2.  The database connection commits and closes.
3.  A fresh connection runs `VACUUM`, reclaiming space.

This ensures the database stays small, fast, and consistent.

------------------------------------------------------------------------

## Timezone Handling

The container mounts the host's timezone files:

    /etc/localtime:/etc/localtime:ro
    /etc/timezone:/etc/timezone:ro

This ensures all dashboard timestamps match the host system.

------------------------------------------------------------------------

## Useful Docker Commands

### Stop the container:

``` bash
docker compose down
```

### Restart the entire stack:

``` bash
docker compose down && docker compose up -d
```

### Open a shell inside the container:

``` bash
docker exec -it pycudawatch bash
```

### Check the GPU from inside the container:

``` bash
docker exec -it pycudawatch nvidia-smi
```

------------------------------------------------------------------------

## License

MIT License.

