#!/usr/bin/env python3
from kafka import KafkaConsumer, KafkaAdminClient
from kafka.errors import KafkaError
from constant import constants
#from data_class.topic_data_classes import TopicCreationResult, Status
from utils.kafka_errors import extract_error_message
from .auth_data_class import AuthResponse

def auth() -> AuthResponse:
    try:
        admin = KafkaAdminClient(bootstrap_servers=constants.BOOTSTRAP_SERVERS)
        return AuthResponse.success(admin)
    except KafkaError as e:
        return AuthResponse.error(f"Kafka connection failed: '{e}'")
    except Exception as e:
        return AuthResponse.error(f"Unexpected auth error: '{e}'")
