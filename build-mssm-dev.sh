#!/bin/bash
cd /home/caddy/mssm-test/
git reset --hard HEAD
start=`git log -1 --format="%H"`
if [ $1 == $start ]
then
echo "look like pulled,skip this time."
exit 0
fi
git pull
sed -i 's/api/test/g' config/prod.env.js
rm -r dist/
npm i
npm audit fix
npm run build
rm -rf /var/mssm-test/*
cp -rf  dist/* /var/mssm-test
