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
COPY working_req.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r working_req.txt

# Copy project files (everything including check/ and dashboard/)
COPY . .

# Set working directory to your app folder
WORKDIR /app/ai-dashboard/dashboard

# Expose port for Cloud Run
EXPOSE 8501

# Run Streamlit app (update homepage.py if your entrypoint file is different)
CMD ["streamlit", "run", "homepage.py", "--server.port=8501", "--server.address=0.0.0.0"]
