FROM python:3.11-slim

# Set UTF-8 locale and system encoding
ENV PYTHONIOENCODING=UTF-8 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install required system packages
RUN apt-get update && apt-get install -y \
    git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set default entrypoint
ENTRYPOINT ["python", "main.py"]
