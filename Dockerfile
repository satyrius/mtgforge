# Base image
FROM phusion/baseimage:0.9.11
MAINTAINER Anton Egorov <anton.egoroff@gmail.com>
ENV HOME /root
RUN /etc/my_init.d/00_regen_ssh_host_keys.sh
CMD ["/sbin/my_init"]

EXPOSE 80 22

RUN locale-gen en_US.UTF-8 ru_RU.UTF-8
RUN sed -i -e 's/archive.ubuntu.com/mirror.yandex.ru/' /etc/apt/sources.list
RUN apt-get update && apt-get install -yV \
    gunicorn \
    nginx \
    nodejs \
    nodejs-legacy \
    npm \
    python-dev \
    python-lxml \
    python-openssl \
    python-pil \
    python-pip \
    python-psycopg2 \
    python-twisted \
    ruby \
    git \
    htop \
    postgresql-client-9.3 \
    tree \
    vim

# Install build tools
RUN gem install --no-rdoc --no-ri foreman
RUN npm install -g bower brunch

WORKDIR /tmp/docker_build

# Install backend app dependencies
COPY requirements.txt /tmp/docker_build/
RUN pip install -r requirements.txt

# Install client app dependencies
COPY frontend/package.json /tmp/docker_build/
RUN npm install
COPY frontend/bower.json /tmp/docker_build/
RUN bower install --allow-root

# Build client app
COPY frontend /tmp/docker_build/frontend
WORKDIR /tmp/docker_build
RUN mv node_modules frontend
RUN mv bower_components frontend
WORKDIR frontend
RUN brunch build --production

# Build backend app
COPY backend /tmp/docker_build/backend
WORKDIR /tmp/docker_build/backend
RUN find -name '*.pyc' -delete
RUN python -c "import compileall; compileall.compile_dir('.', force=1)" > /dev/null
# TODO version file
ENV DJANGO_SETTINGS_MODULE topdeck.settings.prod
ENV DJANGO_APP_LOGS /var/log/mtgforge
ENV DJANGO_APP_ROOT /var/www/mtgforge
ENV DJANGO_MEDIA_ROOT /var/www/mtgforge-media
ENV DJANGO_STATIC_ROOT /var/www/mtgforge-static
RUN mkdir -p /var/www $DJANGO_STATIC_ROOT $DJANGO_MEDIA_ROOT $DJANGO_APP_LOGS
RUN chown www-data $DJANGO_STATIC_ROOT $DJANGO_MEDIA_ROOT $DJANGO_APP_LOGS
RUN setuser www-data ./manage.py collectstatic --noinput --clear

# Web server setup
RUN mv /tmp/docker_build/backend $DJANGO_APP_ROOT
COPY Procfile /var/www/mtgforge/
WORKDIR /var/www/mtgforge/
RUN chown -R root:root .
RUN foreman export \
    --app=mtgforge \
    --log=$DJANGO_APP_LOGS \
    --user=www-data \
    --root=$DJANGO_APP_ROOT \
    runit /etc/service
COPY package/etc /etc
WORKDIR /etc/nginx/sites-enabled
RUN rm default && ln -s ../mtgforge/_.conf mtgforge.conf

# SSH keys of users to login as root
COPY ssh_keys/aeg.pub /tmp/
RUN cat /tmp/aeg.pub >> /root/.ssh/authorized_keys

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
