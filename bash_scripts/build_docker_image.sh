#!/bin/bash

# download code from repository
$ find ./opennebula-kafka-publisher -type d -exec sudo chmod -R 755 {} \;
$ find ./opennebula-kafka-publisher -type f -exec sudo chmod 664 {} \;
$ chmod a+x ./opennebula-kafka-publisher/deployment/run.sh ./opennebula-kafka-publisher/deployment/clean.sh
$ cp ./opennebula-kafka-publisher/deployment/Dockerfile .
# build image
$ sudo docker build --no-cache -t opennebula-kafka-publisher .
$ source opennebula-kafka-publisher/deployment/clean.sh