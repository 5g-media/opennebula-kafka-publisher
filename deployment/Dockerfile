FROM ubuntu:16.04
MAINTAINER Athanasoulis Panagiotis
LABEL version="1.0"

ENV KAFKA_IP=$KAFKA_IP
ENV KAFKA_PORT=$KAFKA_PORT
ENV KAFKA_OPENNEBULA_TOPIC=$KAFKA_OPENNEBULA_TOPIC
ENV KAFKA_TRAFFIC_MANAGER_TOPIC=$KAFKA_TRAFFIC_MANAGER_TOPIC
ENV OSM_IP=$OSM_IP
ENV OSM_USER=$OSM_USER
ENV OSM_PWD=$OSM_PWD
ENV XML_RPC_SERVER=$XML_RPC_SERVER
ENV XML_RPC_SESSION=$XML_RPC_SESSION
ENV SCHEDULER_MINUTES=$SCHEDULER_MINUTES
ENV NO_OSM_VM_IDS=$NO_OSM_VM_IDS

RUN pwd
RUN apt-get update
RUN apt-get -y upgrade

RUN apt-get -y install python3-dev python3-setuptools python3-pip supervisor vim \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir /opt/opennebula-kafka-publisher
COPY opennebula-kafka-publisher /opt/opennebula-kafka-publisher
RUN ls -la /opt/opennebula-kafka-publisher
RUN ls -la /opt/opennebula-kafka-publisher/deployment

RUN pip3 install -r /opt/opennebula-kafka-publisher/requirements.txt \
 && cp /opt/opennebula-kafka-publisher/deployment/publisher.conf /etc/supervisor/conf.d/publisher.conf \
 && rm -rf /etc/supervisor/supervisord.conf \
 && cp /opt/opennebula-kafka-publisher/deployment/supervisor/supervisord.conf /etc/supervisor/supervisord.conf \
 && chmod +x /opt/opennebula-kafka-publisher/deployment/run.sh

EXPOSE 3333

ENTRYPOINT ["/bin/sh"]
CMD ["-c", "/opt/opennebula-kafka-publisher/deployment/run.sh"]
