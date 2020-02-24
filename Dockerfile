# Pull from base image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Set work directory inside docker container
# if we need to run any command inside container,
# docker will run from this directory
WORKDIR /code


# Copy project from local folder where Dockerfile is (.) to
# /code/ directory inside container
COPY . /code/


# Install dependencies
RUN apt-get update
RUN apt-get upgrade -y

RUN pip --retries 5 install --upgrade pip
RUN pip --timeout 15 --retries 5 install -r requirements/local.txt



