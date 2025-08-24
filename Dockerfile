# Use lightweight Python base image
FROM python:3.10-slim

# Install system dependencies (needed for psycopg2, numpy, pandas, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# Copy requirements file
COPY working_req.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r working_req.txt

# Copy app files
COPY . .

# Expose port for Cloud Run
EXPOSE 8501

# Use shell form CMD so $PORT is expanded at runtime
CMD streamlit run homepage.py --server.port=$PORT --server.address=0.0.0.0