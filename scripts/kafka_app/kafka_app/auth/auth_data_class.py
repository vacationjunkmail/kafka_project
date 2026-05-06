#!/usr/bin/env python3
from kafka import KafkaAdminClient
from dataclasses import dataclass
from data_class.base_classes import BaseResponseDataClass
from typing import Optional
from enum import Enum

class Status(Enum):
    SUCCESS = "success"
    ERROR = "error"

@dataclass
class AuthResponse(BaseResponseDataClass):
    admin: Optional[KafkaAdminClient] = None
    is_auth: bool = False

    @classmethod
    def success(cls, admin):
        return cls(status=Status.SUCCESS, message = "Connected", admin = admin, is_auth = True)
    
    @classmethod
    def error(cls,msg):
        return cls(status=Status.ERROR, message=msg, admin=None)
