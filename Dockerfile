# Dockerfile for flask backend

# Use Python 3.11 slim as the base image
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy backend files to /app
COPY controllers/ /app/controllers/
COPY models/ /app/models/
COPY services/ /app/services/
COPY app.py /app/
COPY socket_manager.py /app/
COPY requirements.txt /app/

# Set the PYTHONPATH environment variable to /app
ENV PYTHONPATH=/app

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose backend port
EXPOSE 5000

# Set the working directory back to /app
WORKDIR /app

# Run the backend and frontend processes concurrently
CMD ["python", "app.py"]