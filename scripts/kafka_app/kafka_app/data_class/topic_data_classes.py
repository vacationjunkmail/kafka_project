#!/usr/bin/env python3

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Status(Enum):
    CREATED = "created"
    ERROR = "error"
    EXISTS = "exists"
    DELETED = "deleted"
    NOTEXIST = "open"


@dataclass
class TopicCreationResult:
    topic: str
    status: Optional[Status] = None
    message: str = ""
    created: bool = False
