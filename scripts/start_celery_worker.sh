#! /usr/bin/zsh
cd /home/mobvoi/disk-ext/Downloads/lmproject
source ../lmproject_env/bin/activate
exec celery -A autolm worker -l debug
