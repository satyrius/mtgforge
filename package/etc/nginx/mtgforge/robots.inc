if ($request_uri ~* "^/robots.txt") {
    rewrite ^/robots.txt /static/robots.txt last;
}