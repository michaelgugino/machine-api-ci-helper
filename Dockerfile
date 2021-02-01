# https://github.com/sclorg/s2i-python-container/blob/master/3.8/Dockerfile.fedora

FROM registry.fedoraproject.org/f32/python3:latest

# Set the working directory
WORKDIR /opt/app-root/

# Copy the current directory contents into the container at /music_api
ADD . /opt/app-root/

# Install packages specified in requirements.txt
RUN pip install -r requirements.txt
