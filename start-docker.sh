#!/bin/bash
cd /home/caddy/ims-docker
cp -rf /var/ims/ims-*.jar .
docker build -t ims-spring:$2 .
docker container stop ims-spring
docker run --name ims-spring --rm -v /home/caddy/log:/var/log/ims -p 10000:5000 -d ims-spring:$2
