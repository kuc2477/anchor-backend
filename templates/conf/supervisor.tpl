[program:{{ domain }}]
command=uwsgi
  --socket uwsgi.sock
  --chmod-socket 666
  --processes 1
  --master
  --no-orphans
  --max-requests 5000
  --module {{ module }}
  --callable {{ callable }}
directory={{ root }}
stdout_logfile={{ root }}/uwsgi.log
autostart=true
autorestart=true
redirect-stderr=true
stopsignal=QUIT
