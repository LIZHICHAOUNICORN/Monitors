#! /usr/bin/zsh
cd /home/mobvoi/disk-ext/Downloads/lmproject
source ../lmproject_env/bin/activate
exec gunicorn autolm.wsgi:application -w 8 -k gthread -b 0.0.0.0:8000 --max-requests=10000
