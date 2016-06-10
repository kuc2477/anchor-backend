[program:{{ vhost }}]
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
  --logto {{ uwsgi_logfile }}
directory={{ root }}
autostart=true
autorestart=true
redirect-stderr=true
stdout_logfile={{ uwsgi_logfile }}
stopsignal=QUIT

[program:{{ redis }}]
command={{ runredis }}
directory={{ root }}
autostart=true
autorestart=true
redirect-stderr=true
stdout_logfile={{ redis_logfile }}
stopsignal=QUIT

[program:{{ celery }}]
command={{ runcelery }}
directory={{ root }}
autostart=true
autorestart=true
redirect-stderr=true
stdout_logfile={{ celery_logfile }}
stopsignal=QUIT

[program:{{ router }}]
command={{ runrouter }}
directory={{ root }}
autostart=true
autorestart=true
redirect-stderr=true
stdout_logfile={{ router_logfile }}
stopsignal=QUIT

[program:{{ scheduler }}]
command={{ runscheduler }}
directory={{ root }}
autostart=true
autorestart=true
redirect-stderr=true
stdout_logfile={{ scheduler_logfile }}
stopsignal=QUIT

[program:{{ notifier }}]
command={{ runnotifier }}
directory={{ root }}
autostart=true
autorestart=true
redirect-stderr=true
stdout_logfile={{ notifier_logfile }}
stopsignal=QUIT
