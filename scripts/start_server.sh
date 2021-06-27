#! /usr/bin/zsh
cd /path/to/project
source /conda_env/bin/activate
exec gunicorn autolm.wsgi:application -w 8 -k gthread -b 0.0.0.0:8000 --max-requests=10000
