# *Opennebula-kafka-publisher* service

## Introduction
This service is responsible to:
- retrieve infrastructure monitoring data from the OpenNebula (OnLife) NFVI using the XML-RPC API,
- publish the monitoring data by given VM id (vdu UUID) in the pub/sub broker (Apache Kafka)

Actually, this service feeds the [MAPE](https://github.com/5g-media/mape) with monitoring data.

## Requirements
- Python version 3.5+
- The Apache Kafka broker must be accessible from the service
- The [OSM](https://osm.etsi.org/) (release 5) must be accessible from the service
- The OpenNebula XML-RPC API must be accessible from the service

## Configuration

A variety of variables are defined in the `settings.py`  file. The configuration that is used in the deployment phase (either as `ENV` variables or via an `.env` file in case of docker-compose) includes:

| **Setting** | **Description** |
| --- | --- |
| KAFKA_IP | The host of the Service Platform Virtualization publish/subscribe broker. |
| KAFKA_PORT | The port of the Service Platform Virtualization publish/subscribe broker. By default, port is 9092. |
| KAFKA_OPENNEBULA_TOPIC | The publish/subscribe broker topic name where the monitoring data are published. By default, the topic name is `"nfvi.tid-onlife.opennebula"`. | 
| KAFKA_TRAFFIC_MANAGER_TOPIC | The publish/subscribe broker topic name where the Traffic Manager VM monitoring data are published. The default topic name is `trafficmanager.uc2.metrics`. |
| OSM_IP | The OSM host |
| OSM_USER | The OSM admin user |
| OSM_PWD | The password of the OSM admin user  |
| XML_RPC_SERVER | The host and port of the OpenNebula XML-RPC API |
| XML_RPC_SESSION | The username and password that allows access in the  OpenNebula XML-RPC API |
| SCHEDULER_MINUTES | How frequent the publisher collects the monitoring data through the OpenNebula XML-RPC API and publishes them in the pub/sub broker. Default value is `1` minute. | 
| NO_OSM_VM_IDS | The Virtual Machine IDs (hosted in OpenNebula) from which the service will collect monitoring data. By default, this service collects monitoring data ONLY for the VMs that have been deployed through the OSM. Therefore, this parameter allows you to monitor VMs that haven't deployed through OSM. The value must be string, comma delimeted: e.g. "1002,678,1345" |
 
 ## Installation/Deployment

To build the docker image, copy the bash script included in the `bash_scripts/` folder in the parent folder of the project and then, run:
```bash
$ cd $HOME
# clone repository
$ cp ./opennebula-kafka-publisher/bash_scripts/build_docker_image.sh .
$ chmod +x build_docker_image.sh
$ ./build_docker_image.sh
```

Check the docker images using the cmd:
```bash
$ sudo docker images
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
  -e OSM_PWD="password" \
  -e XML_RPC_SERVER="192.168.83.20:2633" \
  -e XML_RPC_SESSION="user:pass" \
  -e SCHEDULER_MINUTES=1 \
  -e NO_OSM_VM_IDS="1203,1295" \
  -dit opennebula-kafka-publisher
```

Check the running docker containers:
```bash
$ sudo docker ps -a
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
This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement [No 761699](http://www.5gmedia.eu/). The dissemination of results herein reflects only the author’s view and the European Commission is not responsible for any use that may be made of the information it contains.

## License
[Apache 2.0](LICENSE.md)