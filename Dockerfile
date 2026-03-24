# Use a lightweight Python base image
FROM python:3.11-slim

# Disable .pyc files and enable real-time logging (no buffering)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy dependency file first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies without caching to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the application port (used by Docker / cloud platforms like Render)
EXPOSE 5001

# Start the application using Gunicorn (production-grade WSGI server)
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5001", "app:app"]