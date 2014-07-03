#!/bin/bash -e
PROJECT='mtgforge'
PREV_ID=`docker ps | grep $PROJECT | awk '{print $1}'`
[[ -n $PREV_ID ]] && docker stop $PREV_ID 1>/dev/null
docker build -t=$PROJECT .
docker run -d -p 2222:22 -p 8000:80 $PROJECT

BOOT2DOCKER_IP=`boot2docker ip 2>/dev/null`
TCP_PORT_MAPPING=`docker ps -l | grep -Eo ':([0-9]{2,5})->80' | grep -Eo '[0-9]{3,5}'`
SSH_PORT_MAPPING=`docker ps -l | grep -Eo ':([0-9]{2,5})->22' | grep -Eo '[0-9]{3,5}'`

echo "WEB http://$BOOT2DOCKER_IP:$TCP_PORT_MAPPING"
echo "SSH ssh -p $SSH_PORT_MAPPING root@$BOOT2DOCKER_IP"
