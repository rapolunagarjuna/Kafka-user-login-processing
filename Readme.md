# Kafka User Login Statistics Processor

### Running the System
Start the Services:

Use Docker Compose to start all services:

    
    docker-compose up
    

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

Questions:
1. How would you deploy this application in production?
- Containerization: Since most services are already containerized and Docker images are available on Docker Hub, I would also containerize the Python consumer. I would create a Docker image for it and push it to Docker Hub or a private container registry.

- Orchestration with Kubernetes: Kubernetes is an ideal choice for managing containerized applications in production. It provides load balancing, secrets management, automatic restarts, and scaling capabilities.

- Scaling Kafka: To handle increased load, I would scale the number of Kafka brokers from the current single broker. Adding more brokers enhances fault tolerance and load distribution. I would also increase the number of partitions for each topic to handle higher throughput and parallelism. Setting the replication factor to 3 ensures data durability and fault tolerance.

- Topic Management: Instead of relying on automatic topic creation, I would manually create and configure Kafka topics to ensure they meet production requirements and are properly optimized.

- Performance Tuning: I would monitor Kafka’s performance and tune its settings, such as buffer sizes and batch sizes, based on workload and performance metrics.

2. What other components would you want to add to make this production ready?
- Data Processing: Instead of performing processing and statistics calculation within the consumer, which relies on in-memory data and lacks persistence, I would consider using dedicated data processing frameworks. For real-time analytics, Apache Flink or Kafka Streams API are suitable choices. For batch processing, I would dump data into a data lake (e.g., AWS S3, Snowflake) and later use a tool like Apache Airflow to batch load it into a data warehouse (e.g., Spark, Redshift, Hadoop) for further analysis and transformations.

- CI/CD Pipeline: Implement a CI/CD pipeline using tools like Jenkins to automate the build, test, and deployment processes, ensuring consistent and reliable deployments.

- Centralized Logging and Monitoring: Set up centralized logging using Elasticsearch or an alternative logging solution to track and analyze errors and performance issues. Additionally, use resource monitoring tools like Prometheus and Grafana to monitor application health and performance metrics.

3. How can this application scale with a growing dataset?
- Kafka Scaling: Kafka’s design supports scalability with large datasets by persisting events and distributing them across multiple brokers. With Zookeeper managing leader election and broker coordination, the system can scale effectively. Increasing the number of Kafka brokers to three or more will help balance the load and improve fault tolerance. Additionally, partitioning topics and configuring appropriate replication factors will enhance performance and resilience.