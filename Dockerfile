# Use the official Python 3.9 image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the entire backend directory into the Docker image
COPY . .

# Expose port 5001
EXPOSE 5001

# Command to run the FastAPI server
CMD ["python", "./backend/main.py"]
