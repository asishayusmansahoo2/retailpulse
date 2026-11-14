# Use the official Python 3.11 slim image as our base
FROM python:3.10-slim

# Set environment variables to prevent Python from writing bytecode and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first to leverage Docker's caching mechanism
COPY requirements.txt .

# Install dependencies (no-cache-dir keeps the image size small)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the ports Streamlit and MLflow will use
EXPOSE 8501
EXPOSE 5000

# Command to run the Streamlit app when the container starts
CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]