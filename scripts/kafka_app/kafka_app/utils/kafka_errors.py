#!/usr/bin/env python3

import re

def extract_error_message(raw: str) -> str:
    match = re.search(r'error_message="([^"]+)"', raw)
    if match:
        return match.group(1)
    return raw
