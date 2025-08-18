FROM python:3.11-slim

# Install libGL and other required system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
     libgl1 \
    libglx-mesa0 \
    libglib2.0-0 \
    libcom-err2 \
    libp11-kit0 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
