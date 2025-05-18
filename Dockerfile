# Use a lightweight Python image
FROM python:3.11-slim

# Set environment variables to prevent Python from buffering outputs
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Copy requirements file first (to use Docker’s caching mechanism)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the necessary application files
COPY ./src ./src

# Expose port 8000 for external access
EXPOSE 8000

# Ensure the entrypoint script runs with Python
CMD ["python3", "./src/app.py"]
