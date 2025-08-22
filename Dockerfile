# Base image (Debian slim + Python)
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y curl tar texlive pandoc && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy your app and the run.sh script
COPY . .

# Make sure run.sh is executable
RUN chmod +x run.sh

# Install system dependencies if needed inside run.sh
# (run.sh can handle downloading Pandoc or other tools)
RUN ./run.sh

# Expose the port your app runs on
EXPOSE 8000

# Start your app with Gunicorn
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8000"]
