# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# erbose output: Add the --verbose flag to the pip install command in the 
RUN pip install --no-cache-dir --upgrade pip setuptools

# Define environment variable
ENV PYTHONPATH=/app

# Run script.py when the container launches
CMD ["python", "script.py"]
