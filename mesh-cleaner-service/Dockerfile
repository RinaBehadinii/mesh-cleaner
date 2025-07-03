# Use a lightweight Python base image
FROM python:3.11-slim

# Install system-level dependencies (libGL is required for PyMeshLab)
RUN apt-get update && \
    apt-get install -y libgl1 && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
