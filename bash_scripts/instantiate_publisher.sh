#!/bin/bash

sudo docker run -p 80:3333 --name opennebula-kafka-publisher --restart always \
  -e KAFKA_IP="217.172.11.173" \
  -e KAFKA_PORT="9092" \
  -e KAFKA_OPENNEBULA_TOPIC="nfvi.tid-onlife.opennebula" \
  -e KAFKA_TRAFFIC_MANAGER_TOPIC="trafficmanager.uc2.metrics" \
  -e OSM_IP="192.168.83.27" \
  -e OSM_USER="admin" \
  -e OSM_PWD="admin" \
  -e XML_RPC_SERVER="192.168.83.20:2633" \
  -e XML_RPC_SESSION="francesco:francesco00" \
  -e SCHEDULER_MINUTES=1 \
  -e NO_OSM_VM_IDS="677" \
  -dit opennebula-kafka-publisher
