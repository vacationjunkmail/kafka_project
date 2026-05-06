Kafka App
  To run the app.
  Navigate to kafka_demo directory
    This checks to see if the kafka-net is up and creates it if not. Then builds the docker container (kafka, kafka-ui)
    ./build_and_run.sh

    ui address:http://localhost:8092/

    Container is up:
      From host:
        consumer:
          docker exec -it kafka kafka-topics.sh --create --topic from_host --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1 --config retention.ms=600000 --config cleanup.policy=dele    te --config segment.ms=599990
        produer:
          docker exec -it kafka kafka-console-producer.sh --topic from_host --bootstrap-server kafka:9092
      
      From container:
        kafka-topics.sh --create --topic from_host --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1 --config retention.ms=600000 --config cleanup.policy=delete --config segment.ms=599990

        produer:
          kafka-console-producer.sh --topic from_host --bootstrap-server kafka:9092  

  Navigate to python_docker_container:
    check is network is up if not a message displays.
    Brings down the container
    ./build_and_run.sh

    -t is mandatory for all options

    From host:
      Consumer:
        docker exec python-env python /app/kafka_app/kafka_app/main.py -t "Dana1" -c

      Producer:
        One and done:
          docker exec python-env python /app/kafka_app/kafka_app/main.py -t "Dana1" -pc "First Message from python23asdf"
        Streaming:
          docker exec -it python-env python /app/kafka_app/kafka_app/main.py -t "Dana1" -ps
      
      Add Topic:
        docker exec python-env python /app/kafka_app/kafka_app/main.py -t "Dana12" -a

      Delete topic:
        docker exec python-env python /app/kafka_app/kafka_app/main.py -t "Dana13" -d


