# END TO END DEMO: KAFKA -> MONGODB(ON-PREM) -> C2C -> MONGODB (ATLAS)

This is and end to end demo that showcases the following:
- Application producing messages on a **on-prem Kafka broker**. 
- On-prem Kafka Connector setup
- On-prem MongoDB deployment (1 node RS)
- Syncing Data to an Atlas cluster using C2C sync.

The setup is easy and straightforward. The demo leverage the docker engine to run all these components on the same host. 

**Prerequisites**
* AWS account
* SSH client (e.g., PuTTY)
* Docker Compose
* git

**Instructions**
1. Launch a VM on AWS.
2. SCP the `prod/setup` directory to the VM or directly clone the repo from the VM.
3. tar czf setup.tar.gz prod/setup 
4. Install Docker.
5. Start the MongoDB and Kafka containers using Docker Compose.
6. Connect to the MongoDB container and create a sink connector.
7. Start the mongosync process to synchronize the data from the local MongoDB instance to the MongoDB Atlas cluster.
8. Start the producer application to produce data to the local MongoDB instance.

**Steps**

1. Launch a VM on AWS.
    * Create an EC2 instance with the following OS (Ubuntu 20.04 LTS & Min 30GB of storage).  

2. SCP the `setup` directory to the VM.
    * SCP the directory to the VM using the following command:
        `scp -i <Key>.pem -r setup ubuntu@<EC2_Instance>.compute-1.amazonaws.com:/home/ubuntu/demo`

3. Connect to the VM using SSH: `ssh -i <Key>.pem ubuntu@<EC2_Instance>.compute-1.amazonaws.com`
4. Install Docker.
    * Follow the instructions on the Docker website to install Docker on Ubuntu: https://docs.docker.com/engine/install/ubuntu/
5. Start the MongoDB and Kafka containers using Docker Compose.
    * Navigate to the `demo` directory and run the following command:
        `sudo docker compose -p mongo-kafka up -d --force-recreate`
        *To stop all containers and remove images `sudo docker compose -p mongo-kafka down --rmi all`*
6. Connect to the MongoDB container and create a sink connector.
   * Run the following command to connect to the MongoDB container:
        `sudo docker exec -it mongo1 bin/bash`
    * Configure the sink connector found in : `/home/sink_connectorn`
  
  ```
{
  "name": "mongo-tutorial-sink",
  "config": {
    "connector.class": "com.mongodb.kafka.connect.MongoSinkConnector",
    "topics": "<Name of the Kafka Topic>",
    "connection.uri": "mongodb://mongo1",
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": false,
    "database": "<Name of on-prem MongoDB database>",
    "collection": "<Name of on-prem MongoDB collection>"
  }
}
```
 
    * Start the sink connector from the configuration file: `cx simple_sink.json`
    * OPTIONAL: To connect to the local mongodb, run: `mongosh "mongodb://mongo1"`

7. Start the kafka producer application to produce data to the local MongoDB instance.
    * Navigate to the `/home/app` directory.
    * Update `producer.py` to reflect the topic name at you have configured in the connector.c
    * Run the following command to start the producer application:
        `python3 producer.py action=produce`
8. Start the mongosync process to synchronize the data from the local MongoDB instance to the MongoDB Atlas cluster.
    * Run the following command to start the mongosync process:
        `./bin/mongosync \
              --cluster0 "mongodb://mongo1" \
              --cluster1 "mongodb://user:password@<CLUSTER>.mongodb.net:27017,<CLUSTER>.fof1o.mongodb.net:27017,<CLUSTER>.mongodb.net:27017/admin?tls=true"`
    *IMPORTANT: make sure to update the command with your Atlas credentials and the right Cluster Name.
    * start sync: `curl localhost:27182/api/v1/start -XPOST --data '
   {
      "source": "cluster0",
      "destination": "cluster1"
      } '`
   * commit sync: `curl localhost:27182/api/v1/commit -XPOST --data '{ }'`



**Stopping the sync process**

To stop the mongosync process, press `Ctrl`+`C` in the terminal window where it is running.

**Troubleshooting**

If you are having problems with the demo, please consult the @yberrada for assistance.
