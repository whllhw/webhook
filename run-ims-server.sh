#!/bin/bash
export PATH=$PATH:/home/caddy/apache-maven-3.5.3/bin
cd /home/caddy/ims
git reset --hard HEAD
start=`git log -1 --format="%H"`
if [ $1 == $start ]
then
echo "look like pulled,skip this time."
exit 0
fi
git pull
mvn clean package
cp target/ims-*.jar /var/ims/
/etc/init.d/ims restart
