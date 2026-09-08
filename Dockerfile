FROM python:3.12-slim

WORKDIR /app

# System dependencies required by OpenCV and FFmpeg
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY src ./src
COPY config ./config
COPY app.py .
COPY README.md .

# Streamlit port
EXPOSE 8501

# Start the application
CMD ["python", "-m", "streamlit", "run", "app.py", "--server.address=0.0.0.0"]