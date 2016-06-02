[program:{{ program }}]
command={{ uwsgi }}
  --chdir {{ root }}
  --socket uwsgi.sock
  --chmod-socket=666
  --processes 1
  --master
  --no-orphans
  --max-requests=5000
  --module {{ module }}
  --callable {{ callable }}
  --virtualenv {{ virtualenv }}
directory={{ root }}
stdout_logfile={{ uwsgi_logfile }}
autostart=true
autorestart=true
redirect-stderr=true
stopsignal=QUIT
