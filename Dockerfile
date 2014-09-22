# Base image
FROM phusion/baseimage:0.9.13
MAINTAINER Anton Egorov <anton.egoroff@gmail.com>
ENV HOME /root
RUN /etc/my_init.d/00_regen_ssh_host_keys.sh
CMD ["/sbin/my_init"]

RUN locale-gen en_US.UTF-8 ru_RU.UTF-8
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -yV \
    bash-completion \
    command-not-found \
    curl \
    htop \
    postgresql-client-9.3 \
    psmisc \
    tree \
    vim \
        git-core \
        gunicorn \
        nginx \
        nodejs-legacy npm \
        python-dev \
        python-lxml \
        python-openssl \
        python-pil \
        python-pip \
        python-psycopg2 \
        python-twisted \
        ruby \
    && gem install --no-rdoc --no-ri --version=0.74.0 foreman \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN npm install -g bower brunch

EXPOSE 80 22
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
COPY frontend/ /tmp/docker_build/frontend/
RUN mv node_modules frontend \
    && mv bower_components frontend
WORKDIR frontend
RUN find -name '*.swp' -delete \
    && brunch build --production

COPY etc/ /etc/
WORKDIR /etc/nginx/sites-enabled
RUN rm /etc/nginx/sites-enabled/default \
    && ln -s /etc/nginx/mtgforge/_.conf /etc/nginx/sites-enabled/mtgforge.conf \
    && nginx -t \
    && chmod +x /etc/my_init.d/*.sh

ENV DJANGO_SETTINGS_MODULE topdeck.settings.prod
ENV DJANGO_APP_LOGS /var/log/mtgforge
ENV DJANGO_APP_ROOT /var/www/mtgforge
ENV DJANGO_MEDIA_ROOT /var/www/mtgforge-media
ENV DJANGO_STATIC_ROOT /var/www/mtgforge-static

# Build backend app
COPY backend/ /tmp/docker_build/backend/
WORKDIR /tmp/docker_build/backend
RUN mkdir -p /var/www $DJANGO_STATIC_ROOT $DJANGO_MEDIA_ROOT $DJANGO_APP_LOGS \
    && chown www-data $DJANGO_STATIC_ROOT $DJANGO_MEDIA_ROOT $DJANGO_APP_LOGS \
    && setuser www-data ./manage.py collectstatic --noinput --clear \
    && find -name '*.swp' -delete \
    && find -name '*.pyc' -delete \
    && python -c "import compileall; compileall.compile_dir('.', force=1)" > /dev/null \
    && cd .. && mv backend $DJANGO_APP_ROOT

# Web server setup
WORKDIR /var/www/mtgforge
RUN chown -R root:root . \
    && foreman export \
        --app=mtgforge \
        --log=$DJANGO_APP_LOGS \
        --user=www-data \
        --root=$DJANGO_APP_ROOT \
        runit /etc/service
