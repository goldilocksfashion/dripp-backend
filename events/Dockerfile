# Use an official Miniconda runtime as a parent image
FROM continuumio/miniconda3

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in environment.yml
RUN conda env create -f environment.yml

# Activate the environment
SHELL ["conda", "run", "-n", "events", "/bin/bash", "-c"]

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV KAFKA_BROADCAST_SERVERS localhost:9092

# Run app.py when the container launches
CMD ["conda", "run", "-n", "events", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]