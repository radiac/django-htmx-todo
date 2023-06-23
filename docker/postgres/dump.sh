#!/bin/bash
# Dump the database to the backup dir
#
# Usage:
#   docker-compose exec postgres /project/docker/postgres/dump.sh <filename>
#

# If no filename specified, use timestamp
if [ -z "$1" ]; then
    # Timestamp
    FILENAME="$(date + "%Y-%m-%d_%H%M%S").dump"
else
    FILENAME="$1"
fi


if [[ $FILENAME =~ \.dump$ ]]; then
    # If filename ends .dump, do a dump instead
    pg_dump --format=custom --username=$POSTGRES_DB $POSTGRES_DB > /backup/$FILENAME
else
    pg_dump --clean --no-owner --username=$POSTGRES_DB > /backup/$FILENAME
fi
