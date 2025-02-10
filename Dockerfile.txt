FROM python:3.9-slim

WORKDIR /app

# Install required packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all python files and create logs directory
COPY *.py .
RUN mkdir -p logs

# Make logs directory writable
RUN chmod 777 logs

# Set environment variable for logs path
ENV CSV_FILE=/app/logs/metric_log.csv
ENV IMG_FILE=/app/logs/error_distribution.png

# Default command (will be overridden by docker-compose)
CMD ["python", "features.py"]