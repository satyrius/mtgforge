include uwsgi_params;

uwsgi_param HTTPS $https;
uwsgi_param HTTP_SCHEME $scheme;

uwsgi_param USER_AGENT $http_user_agent;
uwsgi_pass_header Authorization;
uwsgi_intercept_errors off;

uwsgi_param UWSGI_CHDIR /var/www/mtgforge/;
uwsgi_param UWSGI_SCRIPT django_wsgi;

uwsgi_param SERVER_NAME mtgforge;

uwsgi_pass 127.0.0.1:3035;
