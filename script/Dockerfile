# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY ./main.py /usr/src/app/
COPY ./schema.py /usr/src/app/
COPY ./requirements.txt /usr/src/app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV POSTGRES_USER='postgres'
ENV POSTGRES_PASSWORD='postgres'
ENV POSTGRES_DBNAME='postgres'

ENV MONGO_INITDB_ROOT_USERNAME='mongo'
ENV MONGO_INITDB_ROOT_PASSWORD='mongo'

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
