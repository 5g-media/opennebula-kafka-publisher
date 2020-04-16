#!/bin/bash

# Set the variables in the supervisor environment
sed -i "s/ENV_KAFKA_IP/$KAFKA_IP/g" /etc/supervisor/supervisord.conf
sed -i "s/ENV_KAFKA_PORT/$KAFKA_PORT/g" /etc/supervisor/supervisord.conf
sed -i "s/ENV_KAFKA_OPENNEBULA_TOPIC/$KAFKA_OPENNEBULA_TOPIC/g" /etc/supervisor/supervisord.conf
sed -i "s/ENV_KAFKA_TRAFFIC_MANAGER_TOPIC/$KAFKA_TRAFFIC_MANAGER_TOPIC/g" /etc/supervisor/supervisord.conf
sed -i "s/ENV_OSM_IP/$OSM_IP/g" /etc/supervisor/supervisord.conf
sed -i "s/ENV_OSM_USER/$OSM_USER/g" /etc/supervisor/supervisord.conf
sed -i "s/ENV_OSM_PWD/$OSM_PWD/g" /etc/supervisor/supervisord.conf
sed -i "s/ENV_XML_RPC_SERVER/$XML_RPC_SERVER/g" /etc/supervisor/supervisord.conf
sed -i "s/ENV_XML_RPC_SESSION/$XML_RPC_SESSION/g" /etc/supervisor/supervisord.conf
sed -i "s/ENV_SCHEDULER_MINUTES/$SCHEDULER_MINUTES/g" /etc/supervisor/supervisord.conf
sed -i "s/ENV_NO_OSM_VM_IDS/$NO_OSM_VM_IDS/g" /etc/supervisor/supervisord.conf

# Restart services
service supervisor start && service supervisor status

# Makes services start on system start
update-rc.d supervisor defaults

echo "Initialization completed."
tail -f /dev/null  # Necessary in order for the container to not stop
