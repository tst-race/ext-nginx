#!/bin/bash
cd /tmp/nginx/nginx-1.14.0
./configure --with-http_ssl_module --add-module=../nginx-rtmp-module
make
make install
touch ~/.rnd
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=raceserver" -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt
openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048 >& /dev/null
cp ../nginx.conf.selfsigned /usr/local/nginx/conf/nginx.conf
cd ..
cp nginx.service /lib/systemd/system/nginx.service
systemctl daemon-reload
systemctl enable nginx.service

