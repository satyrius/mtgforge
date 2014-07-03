# Base image
FROM phusion/baseimage:0.9.11
ENV HOME /root
RUN /etc/my_init.d/00_regen_ssh_host_keys.sh
CMD ["/sbin/my_init"]

EXPOSE 80 22

RUN locale-gen en_US.UTF-8 ru_RU.UTF-8
RUN sed -i -e 's/archive.ubuntu.com/mirror.yandex.ru/' /etc/apt/sources.list
RUN apt-get update && apt-get install -yV \
    git \
    nodejs-legacy \
    nodejs \
    npm \
    vim

# Install all client-side dependencies
RUN npm install -g bower brunch
WORKDIR /var/build/frontend/
COPY frontend/package.json /var/build/frontend/
RUN npm install
COPY frontend/bower.json /var/build/frontend/
RUN bower install --allow-root

# Build client app
COPY frontend /var/build/frontend
RUN brunch build --production

# SSH keys of users to login as root
COPY ssh_keys/aeg.pub /tmp/
RUN cat /tmp/aeg.pub >> /root/.ssh/authorized_keys

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
