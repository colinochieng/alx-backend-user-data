#!/usr/bin/env python3
'''
Module for function that
obfuscates log message
'''
import csv
import logging
import mysql.connector
import os
import re
from typing import List

# Getting field names from the file
file = open('data.csv', encoding='utf-8')
dict_reader = csv.DictReader(file)
fieldnames = dict_reader.fieldnames
PII_FIELDS = tuple(fieldnames[:5])
file.close()


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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]) -> None:
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''
        desc: function to format a record
        return: a formatted string
        '''
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    '''
    desc: function to create a logger instance
        -> The logger should be named "user_data"
            and only log up to logging.INFO level.
        -> It should not propagate messages to other loggers.
        -> It should have a StreamHandle
            with RedactingFormatter as formatter.
    ret: returns a logger instance
    '''
    logger = logging.Logger('user_data', logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.formatter = RedactingFormatter(list(PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.MySQLConnection:
    '''
    desc: function that returns a connector to the database
        (mysql.connector.connection.MySQLConnection object)
    '''
    config = {
        'host': os.environ.get('PERSONAL_DATA_DB_HOST'),
        'user': os.environ.get('PERSONAL_DATA_DB_USERNAME'),
        'password': os.environ.get('PERSONAL_DATA_DB_PASSWORD'),
        'database': os.environ.get('PERSONAL_DATA_DB_NAME')
    }
    # conn = mysql.connector.connect(**config)
    conn = mysql.connector.connection.MySQLConnection(**config)

    return conn


def main() -> None:
    '''
    desc: function that takes no arguments
        -> function will obtain a database connection using
            get_db and retrieve all rows in the users
            table and display each row under a filtered format
    return: None
    '''
    # acquisition of user data from database
    conn_db = get_db()
    cursor = conn_db.cursor()
    cursor.execute("SELECT * FROM users;")

    user_data_string = ''

    # stringified users data collection
    users_data_list = []
    for row in cursor:
        for key, value in zip(fieldnames, row):
            user_data_string += f'{key}={value}; '
        users_data_list.append(user_data_string.strip())
        user_data_string = ''
    cursor.close()
    conn_db.close()

    # logging of data
    logger = get_logger()

    for user_data in users_data_list:
        logger.info(user_data)


if __name__ == '__main__':
    main()
