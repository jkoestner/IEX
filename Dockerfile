# this docker file is used to create a docker image for the web.
# It currently is being built on dockerhub at dmbymdt/folioflex and
# then pulled down into a web container.
# To run dockerfile and create own image `docker build --no-cache -t folioflex .` 
# from where the dockerfile is located.
FROM python:3.8-slim

# Install git
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install chromium (lighter version of Chrome)
RUN apt-get update && \
    apt-get install -y chromium && \
    ln -s /usr/bin/chromium /usr/bin/google-chrome && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /code

# Copy the current directory contents into the container
COPY . .

# Install requirements
RUN pip install . .[gpt] .[web] .[worker]

# Create new user
RUN adduser --disabled-password --gecos '' ffx
RUN chown -R ffx:ffx /code
USER ffx

# Using port 8001 for web
EXPOSE 8001