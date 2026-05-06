#!/usr/bin/env python3
from kafka import KafkaConsumer, KafkaAdminClient, TopicPartition
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError, UnknownTopicOrPartitionError
from constant import constants
from data_class.topic_data_classes import TopicCreationResult, Status
from utils.kafka_errors import extract_error_message
from auth.auth_data_class import AuthResponse
import json

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
    topic_check = ensure_topic(topic, admin)
    if not topic_check.created:
        print(topic_check.message)
        return
    
    consumer = KafkaConsumer(
        bootstrap_servers="kafka:9092",
        consumer_timeout_ms=1000
    )

    print("consumer created", flush=True)

    tp = TopicPartition("from_host", 0)

    consumer.assign([tp])

    print("partition assigned", flush=True)

    consumer.poll(0)

    print("poll completed", flush=True)

    consumer.seek_to_beginning(tp)

    print("seek completed", flush=True)

    while True:
        records = consumer.poll(timeout_ms=1000)

        print(records, flush=True)

        for partition, messages in records.items():
            for msg in messages:
                print(msg.value.decode(), flush=True)