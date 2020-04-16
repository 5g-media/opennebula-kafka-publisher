# *opennebula-kafka-publisher* service

## Introduction
This service is responsible to:
- retrieve infrastructure monitoring data from the OpenNebula (OnLife) NFVI using the XML-RPC API,
- publish the monitoring data by given VM id (vdu UUID) in the pub/sub broker (Apache Kafka)

Actually, this service feeds the [MAPE](https://github.com/5g-media/mape) with monitoring data.

## Requirements
- Python version 3.5+
- The Apache Kafka broker must be accessible from the service
- The OpenNebula XML-RPC API must be accessible from the service

## Configuration
Check the `settings.py` file:
 - *KAFKA_SERVER*: defines the kafka bus *host* and *port*.
 - *KAFKA_CLIENT_ID*: The default value is 'opennebula-kafka-publisher'.
 - *KAFKA_API_VERSION*:The version of the Kafka bus. The default is `(1, 1, 0)`.
 - *KAFKA_OPENNEBULA_TOPIC*: defines the topic in which you want to send the messages. The default topic name is `nfvi.tid-onlife.opennebula`.
 - *KAFKA_TRAFFIC_MANAGER_TOPIC*: defines the topic in which the Traffic Manager VM metrics are sent. The default topic name is `trafficmanager.uc2.metrics`.
 - *OSM_IP*: defines the IP of the OSM
 - *OSM_ADMIN_CREDENTIALS*: defines the admin credentials of the OSM
 - *OSM_COMPONENTS*: defines the OSM services
 - *METRICS_LIST*: declares the set of the metrics that provided from the OpenNebula XML-RPC API. 
 - *SCHEDULER_MINUTES*: defines how frequent the publisher is running to collect the values of the metrics. Default value is `1` minute.
 - *XML_RPC_SERVER*: defines the host & port of the XML-RPC API. The default is `192.168.83.20:2633`.
 - *XML_RPC_SESSION*: defines the session in the XML-RPC API.
 - *NO_OSM_VM_IDS*: defines the VM IDs that are not deployed through the OSM (eg. "1035,1029")
 - *LOGGING*: declares the logging (files, paths, backups, max length)
 
 ## Installation/Deployment

To build the docker image, copy the bash script included in the `bash_scripts/` folder in the parent folder of the project and then, run:
```bash
   chmod +x build_docker_image.sh
   ./build_docker_image.sh
```

Considering the docker image is available, you can deploy the service as a docker container using the below command (check also the `bash_scripts/instantiate_publisher.sh` script):
```bash
$ sudo docker run -p 80:3333 --name opennebula-kafka-publisher --restart always \
  -e KAFKA_IP="192.168.1.175" \
  -e KAFKA_PORT="9092" \
  -e KAFKA_OPENNEBULA_TOPIC="nfvi.tid-onlife.opennebula" \
  -e KAFKA_TRAFFIC_MANAGER_TOPIC="trafficmanager.uc2.metrics" \
  -e OSM_IP="192.168.1.175" \
  -e OSM_USER="admin" \
  -e OSM_PWD="assword" \
  -e XML_RPC_SERVER="192.168.83.20:2633" \
  -e XML_RPC_SESSION="user:pass" \
  -e SCHEDULER_MINUTES=1 \
  -e NO_OSM_VM_IDS="1203,1295" \
  -dit opennebula-kafka-publisher
```
The name of the docker image and container is:  *opennebula-kafka-publisher*.


## Usage
After the installation/deployment of this service, it collects the values of predefined set of metrics 
(as these defined in the `settings.py` file) every `X` minutes and send them in the topic `nfvi.tid-onlife.opennebula`.

## Tests

The entrypoint of the service is the `daemon.py` file.
Thus, you can type the below command to test it without the usage of the docker service after the 
installation of the needed packages (`pip3 install -r requirements.txt`) assuming the usage of python vrs. 3.5:
```bash
$ python3 daemon.py
```

## Authors
- Singular Logic

## Contributors
 - Contact with Authors
 
## Acknowledgements
This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 761699. The dissemination of results herein reflects only the author’s view and the European Commission is not responsible for any use that may be made of the information it contains.

## License
[Apache 2.0](LICENSE.md)