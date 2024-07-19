# Kafka User Login Statistics Processor

### Running the System
Start the Services:

Use Docker Compose to start all services:

    ```
    docker-compose up
    ```

## Overview

This project processes user login data from Kafka topics and generates real-time statistics. It utilizes Apache Kafka for message streaming and maintains an in-memory database to calculate various statistics. 

## Components

### Kafka

- **Kafka Broker**: Configured to listen on ports `9092` (internal) and `29092` (external) for communication.

### Zookeeper

- **Zookeeper**: Configured to listen on port `2181`. It manages the Kafka broker and coordinates Kafka cluster nodes.

### Consumer

The consumer reads messages from the Kafka topic `user-login`, processes the data, and calculates statistics. Key tasks include:

- **Validation**: Ensures messages contain required fields (`user_id`, `device_type`, `device_id`, `locale`, `timestamp`).
- **Processing**: Updates statistics such as login counts per user, device type counts, location counts, and logins by hour.
- **Statistics Calculation**: Computes average logins per user, minimum and maximum logins per user, different device types, different locations, logins at night, and logins in the morning.
- **Publishing**: Sends calculated statistics to the Kafka topic `user-device-stats`.


