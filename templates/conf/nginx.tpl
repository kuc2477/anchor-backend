server {
    listen 80 default_server;
    server_name {{ domain }};
    root {{ root }};

    access_log {{ root }}/access.log;
    error_log {{ root }}/error.log;

    location / {
        include uwsgi_params;
        uwsgi_pass unix://{{ root }}/uwsgi.sock;
    }

    location /static {
        alias {{ root }}/{{ static }};
    }
}
