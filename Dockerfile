# Base image
FROM phusion/baseimage:0.9.11
MAINTAINER Anton Egorov <anton.egoroff@gmail.com>
ENV HOME /root
RUN /etc/my_init.d/00_regen_ssh_host_keys.sh
CMD ["/sbin/my_init"]

EXPOSE 80 22

RUN locale-gen en_US.UTF-8 ru_RU.UTF-8
RUN sed -i -e 's/archive.ubuntu.com/mirror.yandex.ru/' /etc/apt/sources.list
RUN apt-get update && apt-get install -yV git vim tree htop

WORKDIR /tmp/docker_build

# Install client app dependencies
RUN apt-get update && apt-get install -yV nodejs nodejs-legacy npm
RUN npm install -g bower brunch
COPY frontend/package.json /tmp/docker_build/
RUN npm install
COPY frontend/bower.json /tmp/docker_build/
RUN bower install --allow-root

# Install backend app dependencies
RUN apt-get update && apt-get install -yV \
    postgresql-client-9.3 \
    python-dev \
    python-lxml \
    python-openssl \
    python-pil \
    python-pip \
    python-psycopg2 \
    python-twisted
COPY requirements.txt /tmp/docker_build/
RUN pip install -r requirements.txt

# Build client app
COPY frontend /tmp/docker_build/frontend
WORKDIR /tmp/docker_build
RUN mv node_modules frontend
RUN mv bower_components frontend
WORKDIR frontend
RUN brunch build --production

# Build backend app
COPY backend /var/www/mtgforge

# SSH keys of users to login as root
COPY ssh_keys/aeg.pub /tmp/
RUN cat /tmp/aeg.pub >> /root/.ssh/authorized_keys

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
