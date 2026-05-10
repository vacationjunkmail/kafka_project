#!/usr/bin/env python3

from .producer import producer
import json


def send_message(topic: str, msg: str):
    try:
        print(f"'{msg}' sent to '{topic}'")
        producer.send(topic, msg)
    except Exception:
        print(f"The msg:'{msg}' for topic '{topic} failed to send")


def send_message_cli(topic: str, msg: str):
    try:
        print(f"'{msg}' sent to '{topic}'")
        producer.send(topic, msg).get(timeout=10)
    except Exception:
        print(f"The msg:'{msg}' for topic '{topic} failed to send")


def send_json_message(topic: str, msg: dict):
    msg_str = json.dumps(msg)
    try:
        print(f"'{msg_str}' sent to '{topic}'")
        producer.send(topic, msg_str)
    except Exception:
        print(f"The msg:'{msg}' for topic '{topic} failed to send")
