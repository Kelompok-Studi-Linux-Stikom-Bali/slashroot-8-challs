#!/bin/env bash

export $(grep -v '^#' .env | xargs)

sudo docker build . -t angelchan
[[ `sudo docker ps -qf name=${APP_NAME}` ]] && sudo docker stop ${APP_NAME}
sudo docker run -tid --rm --name ${APP_NAME} -p ${PORT}:80 angelchan

echo "Setup ${APP_NAME} on port ${PORT}"
