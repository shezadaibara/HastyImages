# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.7

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /image_service

# Set the working directory to /rss_service
WORKDIR /image_service

# Copy the current directory contents into the container at /rss_service
ADD . /image_service/

RUN pwd
# Install any needed packages specified in requirements.txt
RUN pip install -r ./application/requirements.txt
