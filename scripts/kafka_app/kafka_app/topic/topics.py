#!/usr/bin/env python3
from kafka import KafkaConsumer, KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError, UnknownTopicOrPartitionError
from constant import constants
from data_class.topic_data_classes import TopicCreationResult, Status
from utils.kafka_errors import extract_error_message
from auth.auth_data_class import AuthResponse
import json
import time

def ensure_topic(topic:str, admin: AuthResponse) -> TopicCreationResult:

    results = TopicCreationResult(topic = topic)

    try:
        is_available = admin.describe_topics([topic])
        
        if is_available[0]['error_code'] == 0:
            results.status = Status.EXISTS.value
            results.message = f"Topic '{topic}' already exists"
            results.created = True
        else:
            results.status = Status.NOTEXIST.value
            results.message = f"Topic '{topic}' does not exist"
    except UnknownTopicOrPartitionError as e:
        results.status = Status.ERROR.value
        results.message = f"Topic was not able to be described:'{str(e)}'"
    except Exception as e:
        results.status = Status.ERROR.value
        results.message = str(e)
    return results

def create_topic(topic:str, admin: AuthResponse) -> TopicCreationResult:
    topic_check = ensure_topic(topic, admin)
    if topic_check.created:
        return topic_check
    results = TopicCreationResult(topic = topic)
    try:
        admin.create_topics([NewTopic(name=topic,num_partitions=constants.PARTITIONS,replication_factor=constants.REPLICATION, topic_configs = {"retention.ms":constants.RETENTION,"cleanup.policy":constants.POLICY, "segment.ms": constants.SEGMENT})])
        results.status = Status.CREATED.value
        results.message = f"Topic '{topic}' created"
        results.created = True
        return results
    except TopicAlreadyExistsError as e:
        results.status = Status.EXISTS.value
        results.message = extract_error_message(e.args[0])
        return results
    except Exception as e:
        results.status = Status.ERROR.value
        results.message = str(e)
        return results

def delete_topic(topic:str, admin: AuthResponse) -> TopicCreationResult:
    topic_check = ensure_topic(topic, admin)
    if not topic_check.created:
        return topic_check
    results = TopicCreationResult(topic = topic)
    try:
        admin.delete_topics([topic])
        results.status = Status.DELETED.value
        results.message = f"Topic {topic} was {Status.DELETED.value}"
    except UnknownTopicOrPartitionError as e:
        results.status = Status.ERROR.value
        results.message = str(e)
    return results

def consume (topic: str, admin):
    # topic_check = ensure_topic(topic, admin)
    # if not topic_check.created:
    #     print(topic_check.message)
    #     return 
    results = create_topic(topic, admin)
    print(results.message)
    consumer = KafkaConsumer(
    topic,
    bootstrap_servers=constants.BOOTSTRAP_SERVERS,
    auto_offset_reset="earliest",
    )

    print(f"Connected and consuming: {topic}", flush=True)

    for msg in consumer:
        print(f"{msg.value.decode()}", flush=True)

def producer_cli(topic: str, msg: str, admin):
    topic_check = ensure_topic(topic, admin)
    if not topic_check.created:
        print(topic_check.message)
        return ""
    print(f"{topic}:{msg}")
    producer = KafkaProducer(
        bootstrap_servers=constants.BOOTSTRAP_SERVERS,
        value_serializer=lambda v: v.encode("utf-8"),
    )

    producer.send(topic,msg)
    producer.flush()
    print(f"'{msg}' sent to '{topic}'")

def producer_stream(topic: str):
    producer = KafkaProducer(
        bootstrap_servers=constants.BOOTSTRAP_SERVERS,
        value_serializer=lambda v: v.encode("utf-8"),
    )

    while True:
        try:
            msg = input()
            producer.send(topic, msg)
            producer.flush()
        except KeyboardInterrupt:
            print("Goodbye", flush=True)
            break

def production_watcher(topic: str, log_file,admin:AuthResponse):
    producer = KafkaProducer(
        bootstrap_servers=constants.BOOTSTRAP_SERVERS,
        value_serializer=lambda v: v.encode("utf-8"),
    )
    for line in tail_file(log_file):
        producer.send(topic,line)
        producer.flush()

def tail_file(path:str):
    with open(path, "r") as f:
        f.seek(0,2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(.3)
                continue
            yield line.rstrip("\n")