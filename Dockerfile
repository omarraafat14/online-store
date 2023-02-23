# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory to /app
RUN mkdir /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install the dependencies needed for mysqlclient
# RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential
# RUN apt-get install default-mysql-client -y

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Install nginx and supervisor
RUN apt-get update && apt-get install -y nginx supervisor && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy nginx and supervisor configuration files
COPY nginx.conf /etc/nginx/nginx.conf
# COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Make port 8000 and 80 available to the world outside this container
EXPOSE 8000
EXPOSE 80

# Define environment variable
ENV NAME task
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Run supervisor to start both Django and Nginx
# CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
