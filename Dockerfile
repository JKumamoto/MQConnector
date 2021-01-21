# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /code

# install MQ
RUN mkdir -p /opt/mqm/
COPY 9.1.5.0-IBM-MQC-Redist-LinuxX64.tar.gz .
RUN tar -vxf 9.1.5.0-IBM-MQC-Redist-LinuxX64.tar.gz -C /opt/mqm/
RUN rm 9.1.5.0-IBM-MQC-Redist-LinuxX64.tar.gz
ENV LD_LIBRARY_PATH /opt/mqm/lib64:$LD_LIBRARY_PATH

# install VIM
RUN apt-get update && apt-get install -y \
	vim \
	curl \
	&& rm -rf /var/lib/apt/lists/*

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/ .

# command to run on container start
CMD [ "python", "-u", "./mq.py" ] 
