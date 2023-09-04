#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

wait_psql.sh
collectstatic.sh
migrate.sh
init_superuser.sh
runserver.sh