#!/bin/bash
export PATH=$PATH:/home/caddy/apache-maven-3.5.3/bin
cd /home/caddy/ims-test
git reset --hard HEAD
start=`git log -1 --format="%H"`
if [ $1 == $start ]
then
echo "look like pulled,skip this time."
exit 0
fi
git pull
mvn clean package
cp target/ims-*.jar /home/caddy/ims-docker
if [ $(docker ps | grep ims-test | awk '{print $1}') ]
then
docker stop ims-test
fi
cd /home/caddy/ims-docker
docker build -t ims-test .
docker run --rm -d --name ims-test -v /home/caddy/log:/var/log/ims -p 127.0.0.1:10000:10000 ims-test

