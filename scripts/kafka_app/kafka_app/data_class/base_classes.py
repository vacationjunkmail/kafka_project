#!/usr/bin/env python3

from dataclasses import dataclass


@dataclass
class BaseResponseDataClass:
    status: str | None
    message: str = ""
