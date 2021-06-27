#! /usr/bin/zsh
cd /path/to/project
source ../conda_env/bin/activate
exec celery -A monitors flower --port=5555 -l debug
