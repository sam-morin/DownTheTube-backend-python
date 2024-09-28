# Use an official Python runtime as a parent image
FROM python:3.13.0rc2-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install FFmpeg (using Debian's package manager)
RUN apt-get update && apt-get install -y ffmpeg

# Make port 5001 available to the world outside this container
EXPOSE 5001 
# Change this to the port that you want to use externally, if you need to change it. 5001 will work.

# Run server.py when the container launches
CMD ["python", "server.py"]
