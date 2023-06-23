#!/bin/bash
set -e

cd /project/winterhelm

./manage.py migrate
./manage.py runserver 0:8000
