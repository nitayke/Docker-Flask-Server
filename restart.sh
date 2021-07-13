#!/bin/bash

docker rm -f flask_container
docker build -t flask_server .
docker run -d -p 5000:5000 -v /home/lambda-sim/sandbox/indoors_server_farm/bags/:/bags/ --name flask_container flask_server
