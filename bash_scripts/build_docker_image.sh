#!/bin/bash

find ./opennebula-kafka-publisher -type d -exec chmod -R 755 {} \;
find ./opennebula-kafka-publisher -type f -exec chmod 664 {} \;
chmod a+x ./opennebula-kafka-publisher/deployment/run.sh ./opennebula-kafka-publisher/deployment/clean.sh
cp ./opennebula-kafka-publisher/deployment/Dockerfile .
sudo docker build --no-cache -t opennebula-kafka-publisher .
source opennebula-kafka-publisher/deployment/clean.sh