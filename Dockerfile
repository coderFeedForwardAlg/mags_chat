# Use the official Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY reqs.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r reqs.txt

# Copy the application code to the working directory
COPY . .

# Expose the port on which the application will run
# Run the FastAPI application using uvicorn server
CMD ["fastapi", "run", "query_data.py", "--port", "80"]
