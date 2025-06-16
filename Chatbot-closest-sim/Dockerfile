# Use an official Python runtime as a parent image
FROM python:3.13.5-slim

# Set the working directory to /app
WORKDIR /chatbot

# Copy the current directory contents into the container at /app
COPY . /chatbot

# Install any needed packages specified in requirements.txt
RUN /usr/local/bin/python -m pip install --trusted-host pypi.python.org -r /chatbot/requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=Chatbot.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

