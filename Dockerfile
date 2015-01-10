# Base image
FROM phusion/baseimage:0.9.15
MAINTAINER Anton Egorov <anton.egoroff@gmail.com>
ENV HOME /root
RUN /etc/my_init.d/00_regen_ssh_host_keys.sh
CMD ["/sbin/my_init"]

RUN locale-gen en_US.UTF-8 ru_RU.UTF-8 \
    && apt-get update -qq \
    && DEBIAN_FRONTEND=noninteractive apt-get install -qq \
        bash-completion \
        command-not-found \
        curl \
        htop \
        postgresql-client-9.3 \
        psmisc \
        tree \
        vim \
            build-essential \
            git-core \
            gunicorn \
            libssl-dev \
            nginx \
            python-cffi \
            python-dev \
            python-lxml \
            python-openssl \
            python-pil \
            python-pip \
            python-psycopg2 \
            python-pycparser \
            python-twisted \
            ruby \
    && gem install --no-rdoc --no-ri --version=0.74.0 foreman \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


EXPOSE 80
WORKDIR /tmp/docker_build

# Install backend app dependencies
COPY requirements.txt /tmp/docker_build/
COPY requirements-crawl.txt /tmp/docker_build/
RUN pip install -r requirements.txt -r requirements-crawl.txt

COPY etc/ /etc/
RUN find . -name '*.swp' -delete \
    && nginx -t \
    && chmod +x /etc/my_init.d/*.sh

ENV DJANGO_SETTINGS_MODULE topdeck.settings.prod
ENV DJANGO_APP_ROOT /var/www/mtgforge
ENV DJANGO_STATIC_ROOT /var/www/mtgforge-static
VOLUME = [ \
    "/var/www/mtgforge-media/", \
    "/var/log/mtgforge/", \
    "/var/log/nginx/"]

# Build backend app
COPY backend/ /tmp/docker_build/backend/
WORKDIR /tmp/docker_build/backend
RUN mkdir -p /var/www $DJANGO_STATIC_ROOT \
    && chown www-data $DJANGO_STATIC_ROOT \
    && setuser www-data ./manage.py collectstatic --noinput --clear \
    && find . -name '*.swp' -delete \
    && find . -name '*.pyc' -delete \
    && python -c "import compileall; compileall.compile_dir('.', force=1)" > /dev/null \
    && cd .. && mv backend $DJANGO_APP_ROOT

# Web server setup
WORKDIR /var/www/mtgforge
RUN chown -R root:root . \
    && foreman export \
        --app=mtgforge \
        --log=/var/log/mtgforge \
        --user=www-data \
        --root=$DJANGO_APP_ROOT \
        runit /etc/service
