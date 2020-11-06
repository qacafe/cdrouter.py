#!/bin/bash

IMAGE=python:3.5

GIT_USER_NAME=$(git config user.name)
GIT_USER_EMAIL=$(git config user.email)

TWINE_USERNAME=$(grep username ~/.pypirc | sed -e 's/username = //')
TWINE_PASSWORD=$(grep password ~/.pypirc | sed -e 's/password = //')

if [[ $# -ge 2 && "$1" = "-image" ]];
then
    IMAGE=$2
    shift 2
fi

WORKDIR=/usr/src/myapp

docker pull ${IMAGE}
docker run -it --rm -v ${PWD}:${WORKDIR} -w ${WORKDIR} \
       -e GIT_USER_NAME="${GIT_USER_NAME}"   \
       -e GIT_USER_EMAIL="${GIT_USER_EMAIL}" \
       -e TWINE_USERNAME="${TWINE_USERNAME}" \
       -e TWINE_PASSWORD="${TWINE_PASSWORD}" \
       ${IMAGE} /usr/src/myapp/manage.sh git-config clean setup "$@"
