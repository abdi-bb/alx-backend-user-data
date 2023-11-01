#!/usr/bin/env python3
'''
Module: 'filtered_logger'
Function that returns the log message obfuscated
'''

import mysql.connector
import os
import logging
from typing import List
import re

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    '''Returns the log message obfuscated'''
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}',
                         message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        '''Instantiation'''
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''Filter values in incoming log'''
        return filter_datum(
            self.fields,
            self.REDACTION,
            super().format(record),
            self.SEPARATOR
        )


def get_logger() -> logging.Logger:
    '''Returns a logging.logger object'''
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()

    formatter = RedactingFormatter(fields=PII_FIELDS)

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''Returns a connector to a db'''
    db_username = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.environ.get("PERSONAL_DATA_DB_NAME", "holberton")

    try:
        db = mysql.connector.connect(
            user=db_username,
            password=db_password,
            host=db_host,
            database=db_name
        )
        return db
    except mysql.connector.Error as err:
        print(f'Error: {err}')
        return None
