# Build Docker container for ios-tools
# docker build -t iostools/test .
# docker run -it iostools/test
FROM ubuntu:16.04
MAINTAINER matteyeux

RUN apt-get update
RUN apt-get install git python-pip -y
RUN git clone https://github.com/matteyeux/ios-tools
RUN pip install -r /ios-tools/requirements.txt
