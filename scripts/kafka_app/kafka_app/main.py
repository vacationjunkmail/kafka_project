#!/usr/bin/env python3

from topic.topics import (
    delete_topic,
    create_topic,
    consume,
    producer_cli,
    producer_stream,
    production_watcher,
)
from cli.cli import parse_args
from auth.auth import auth


def main():
    args = parse_args()
    topic = args.topic
    topic_delete = args.delete
    topic_add = args.add

    auth_results = auth()

    if topic_delete and topic_add:
        print("Both -a (add topic) and -d (delete topic) can not be true")
    elif not auth_results.is_auth or auth_results is None:
        print(auth_results.message)
    elif topic_add and auth_results.is_auth:
        results = create_topic(topic, auth_results.admin)
        print(results.message)
    elif topic_delete and auth_results.is_auth:
        delete_results = delete_topic(topic, auth_results.admin)
        print(delete_results.message)
    elif args.consume:
        consume(topic, auth_results.admin)
    elif args.producer_cli:
        producer_cli(topic, args.producer_cli, auth_results.admin)
    elif args.producer_stream:
        producer_stream(topic, auth_results.admin)
    elif args.production:
        production_watcher(topic, "/var/log/test.log", auth_results.admin)


if __name__ == "__main__":
    main()
