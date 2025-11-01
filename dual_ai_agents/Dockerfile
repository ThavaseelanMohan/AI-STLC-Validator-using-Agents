# Use an official Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements first (to leverage Docker layer caching)
COPY requirements.txt /app/

# Install system dependencies and Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
    && pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

# Copy the rest of your application code
COPY . /app

# Expose Streamlit’s default port
EXPOSE 8501

# Set environment variables (for Streamlit to run smoothly)
ENV PATH="/usr/local/bin:$PATH"
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV PYTHONUNBUFFERED=1

# Debug step (optional)
# RUN python -m pip show streamlit

# Use python -m to ensure we use the correct interpreter
CMD ["python", "-m", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
