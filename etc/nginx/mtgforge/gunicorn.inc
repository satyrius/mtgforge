proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Remote_Addr $remote_addr;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_set_header Host $http_host;

proxy_set_header USER_AGENT $http_user_agent;

proxy_redirect off;

set $myscheme $scheme;
if ($http_x_url_scheme) {
    set $myscheme $http_x_url_scheme;
}
proxy_set_header X-Url-Scheme $myscheme;

proxy_connect_timeout 15s;
proxy_read_timeout 15s;
proxy_send_timeout 15s;

proxy_pass http://gunicorn_backend;
