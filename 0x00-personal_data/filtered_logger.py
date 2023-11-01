#!/usr/bin/env python3
'''
Module for function that
obfuscates log message
'''
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    '''
    desc: function that use a regex to replace
        occurrences of certain field values
    params:
        fields: a list of strings
            representing all fields to obfuscate
        redaction: a string representing by
            what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is
            separating all fields in the log line (message)
    return: the log message obfuscated
    '''
    for field in fields:
        pattern = rf'{field}=(.*?)(?={separator}|$)'
        message = re.sub(pattern, f'{field}={redaction}', message)
    return message
