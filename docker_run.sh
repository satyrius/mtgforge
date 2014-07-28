#!/bin/bash -e
PROJECT='mtgforge'
PREV_ID=`docker ps | grep $PROJECT | awk '{print $1}'`
[[ -n $PREV_ID ]] && docker stop $PREV_ID 1>/dev/null
docker build --rm -t=$PROJECT .

DB_HOST=`boot2docker config 2>/dev/null | grep HostIP | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}'`
docker run -d \
    -e DATABASE_URL="postgres://$USER@$DB_HOST/mtgforge" \
    -p 1022:22 -p 8000:80 $PROJECT

BOOT2DOCKER_IP=`boot2docker ip 2>/dev/null`
TCP_PORT_MAPPING=`docker ps -l | grep -Eo ':([0-9]{2,5})->80' | grep -Eo '[0-9]{3,5}'`
SSH_PORT_MAPPING=`docker ps -l | grep -Eo ':([0-9]{2,5})->22' | grep -Eo '[0-9]{3,5}'`

echo "http://$BOOT2DOCKER_IP:$TCP_PORT_MAPPING"
echo "ssh -p $SSH_PORT_MAPPING root@$BOOT2DOCKER_IP"
