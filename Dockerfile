# Use a base image with Python 3.12 support
FROM python:3.12-slim

# Install system dependencies for image processing & audio processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    imagemagick \
    fluidsynth \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy our bot code into the container
COPY . .

# Run your bot
CMD ["python", "-u", "tohru.py"]
