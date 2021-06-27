#! /usr/bin/zsh
cd /path/to/project
source /conda_env/bin/activate
exec celery -A monitors beat -l debug
