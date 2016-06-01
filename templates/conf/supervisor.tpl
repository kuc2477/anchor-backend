[program:{{ domain }}]
command=uwsgi
  --socket uwsgi.sock
  --processes 1
  --master
  --no-orphans
  --max-requests 5000
  --module {{ module }}
  --callable {{ callable }}
directory={{ root }}
stdout_logfile={{ uwsgi_logfile }}
autostart=true
autorestart=true
redirect-stderr=true
stopsignal=QUIT
