# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Install build essentials for pyarrow if needed, though 3.11-slim usually has wheels
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV PORT=8080

# Run ui.py when the container launches
CMD ["streamlit", "run", "src/ui.py", "--server.port=8080", "--server.address=0.0.0.0"]
