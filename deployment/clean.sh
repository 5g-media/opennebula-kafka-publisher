#!/bin/bash

# Check if container is running
if sudo docker ps | grep -q 'opennebula-kafka-publisher'; then
    # Gracefully stop supervisor
    sudo docker exec -i opennebula-kafka-publisher service supervisor stop && \
    sudo docker stop opennebula-kafka-publisher && \
    sudo docker rm -f opennebula-kafka-publisher
fi
