#!/usr/bin/env python3

import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Kafka Topic Parse")
    parser.add_argument("-t", "--topic", required=True)
    parser.add_argument("-d", "--delete", action="store_true", help="Delete Topic")
    parser.add_argument("-a", "--add", action="store_true", help="Add Topic")
    parser.add_argument("-c", "--consume", action="store_true", help="Consume Topic")
    parser.add_argument("-pc", "--producer_cli", help="Producer runs once")
    parser.add_argument(
        "-ps", "--producer_stream", action="store_true", help="Producer is streaming"
    )
    parser.add_argument(
        "-p", "--production", action="store_true", help="Production to stream a file"
    )
    return parser.parse_args()
