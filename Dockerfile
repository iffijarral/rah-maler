# Stage 1: Build Tailwind CSS
FROM node:20.13.1 AS builder

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json* ./

# Install Node.js dependencies
RUN npm install

# Copy the CSS folder and other necessary files
COPY . .

# Build the Tailwind CSS
RUN npm run build:css

# Stage 2: Setup Python Environment
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js in the Python image
RUN apt-get update && apt-get install -y curl && \
    curl -sL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy built Tailwind CSS from builder stage
COPY --from=builder /app/css/output.css ./css/output.css

# Expose the application port
EXPOSE 8080

# Run the Bottle application
CMD ["python", "app.py"]
