#!/usr/bin/env python3

from kafka import KafkaProducer
from constant import constants

producer = KafkaProducer(
    bootstrap_servers=constants.BOOTSTRAP_SERVERS,
    value_serializer=lambda v: v.encode("utf-8"),
)
