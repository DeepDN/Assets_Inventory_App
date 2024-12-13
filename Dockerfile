FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install system dependencies required by psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir flask flask-sqlalchemy psycopg2

# Expose the application port
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
