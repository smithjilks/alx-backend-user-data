#!/usr/bin/env python3
""" This script contains a function called filter_datum
that returns the log message obfuscated
"""
import logging
import mysql.connector
from os import environ
import re
from typing import List


PII_FIELDS = ["name", "email", "phone", "ssn", "password",
              "ip", "last_login", "user_agent"]

def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    fields: a list of strings representing all fields to obfuscate
    redaction: a string representing by what the field will be obfuscated
    message: a string representing the log line
    separator: a string representing by which character is separating all
    fields in the log line (message)
    """
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Constructor"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Implements the format method to filter values in incoming
        log records using filter_datum. Values for fields in fields should be
        filtered """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """ function that takes no arguments
    and returns a logging.Logger object. """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ function that returns a connector
    to the database (mysql.connector.connection.MySQLConnection object).
    """
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")

    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")


    connection = mysql.connector.connection.MySQLConnection(user=username,
                                                     password=password,
                                                     host=host,
                                                     database=db_name)
    return connection





def main():
    """
    This function obtains a database connection using get_db
    and retrieves all rows in the users table
    and display each row under a filtered format
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    field_names = [i[0] for i in cursor.description]

    logger = get_logger()

    for row in cursor:
        fmt_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, field_names))
        logger.info(fmt_row.strip())

    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
