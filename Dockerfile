# Using basic image of Python
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Installing system dependencies for working with PostgreSQL
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies
COPY requirements.txt .

# Installing Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Opening a port for the application
EXPOSE 8000

# Setting the default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]