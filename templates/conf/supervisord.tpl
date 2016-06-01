[unix_http_server]
file={{ socket }}                   ; path to your socket file

[supervisorctl]
serverurl=unix://{{ socket }}       ; use a unix:// URL  for a unix socket

[supervisord]
logfile={{ logfile }}               ; supervisord log file
logfile_maxbytes=50MB               ; maximum size of logfile before rotation
logfile_backups=10                  ; number of backed up logfiles
loglevel=error                      ; info, debug, warn, trace
pidfile={{ pidfile }}               ; pidfile location
nodaemon=false                      ; run supervisord as a daemon
minfds=1024                         ; number of startup file descriptors
minprocs=200                        ; number of process descriptors
user=root                           ; default user
childlogdir={{ childlogdir }}       ; where child log files will live

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[include]
files = /etc/supervisor/conf.d/*.conf
