# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    git-lfs \
    ffmpeg \
    libsm6 \
    libxext6 \
    cmake \
    rsync \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copy all files
COPY . .

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (HF Spaces uses 7860)
EXPOSE 7860

# Start FastAPI server (MANDATORY for OpenEnv validation)
CMD ["uvicorn", "inference:app", "--host", "0.0.0.0", "--port", "7860"]