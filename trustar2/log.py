# Seems like from time to time people do a from trustar2 import *, lets minimize the chances of something ugly happening
__all__ = ["get_logger", "TrustarJSONFormatter"]

import datetime
import logging
import logging.handlers
import os
import sys

import json_log_formatter

from .config import (
    LOGGING_LEVEL_VAR,
    LOGGING_SHOW_LEVEL_VAR,
    LOGGING_SHOW_MODULE_VAR,
    LOGGING_SHOW_TIME_VAR,
    LOGGING_SHOW_STASH_INFO_VAR,
    LOGGING_FILENAME_VAR,
    LOGGING_STDOUT_ENABLED_VAR,
)

DEFAULT_LOGGING_LEVEL = logging.INFO

class TrustarJSONFormatter(json_log_formatter.JSONFormatter):
    """
    Custom class to override the default behaviour of the JSONFormatter
    """

    def __init__(self, stash_config=None):
        super(TrustarJSONFormatter, self).__init__()
        self._stash_config = stash_config

    def format(self, record):
        """
        the default behaviour of JSONFormatter is to cast everything into a string
        we avoid calling getMessage and leave the object as it is, this way our json messages can have nested dicts
        """
        message = record.msg
        extra = self.extra_from_record(record)
        json_record = self.json_record(message, extra, record)
        # Backwards compatibility: Functions that overwrite this but don't
        # return a new value will return None because they modified the
        # argument passed in. --v
        mutated_record = self.mutate_json_record(json_record) or json_record
        return self.to_json(mutated_record)

    def json_record(self, message, extra, record):
        extra['message'] = message

        extra = self._add_system_logs_to_json(extra, record)
        extra = self._add_stash_logs_to_json(extra)
        if record.exc_info:
            extra['exec_info'] = self.formatException(record.exc_info)
        return extra

    def _add_stash_logs_to_json(self, extra):
        if not int(os.environ.get(LOGGING_SHOW_STASH_INFO_VAR, 1)):
            return extra
        if not self._stash_config:
            return extra
        
        extra['stash_type'] = self._stash_config.get("stash_type", "UNKNOWN")
        extra['stash_name'] = self._stash_config.get("stash_name", 'UNKNOWN')
        extra['stash_id'] = self._stash_config.get("stash_id", 'UNKNOWN')
        extra['enclave_ids'] = self._stash_config.get("enclave_ids", 'UNKNOWN')

        return extra

    def _add_system_logs_to_json(self, extra, record):
        if int(os.environ.get(LOGGING_SHOW_LEVEL_VAR, 1)):
            extra['level'] = record.levelname
        
        if int(os.environ.get(LOGGING_SHOW_MODULE_VAR, 1)):
            extra['module'] = record.name
        
        if int(os.environ.get(LOGGING_SHOW_TIME_VAR, 1)):
            extra['time'] = datetime.datetime.utcnow()
        
        return extra

    def to_json(self, record):
        """Converts record dict to a JSON string.

        It makes best effort to serialize a record (represents an object as a string)
        instead of raising TypeError if json library supports default argument.
        Note, ujson doesn't support it.
        """
        return self.json_lib.dumps(record, default=_json_object_encoder)


def _json_object_encoder(obj):
    try:
        return obj.to_json()
    except AttributeError:
        return str(obj)


def get_stdout_handler(formatter):
    """
    Gets the handler to manage the output of the logger, default: stdout
    """
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    return handler

def get_file_handler(filename, formatter):
    handler = logging.handlers.RotatingFileHandler(
                filename=filename,
                mode='a',
                maxBytes=8192000,
                backupCount=10,
        )
    handler.setFormatter(formatter)
    return handler


def get_formatter(stash_config=None):
    return TrustarJSONFormatter(stash_config=stash_config)

def get_log_file(filename=None):
    """
        Return the log file filename if its set.
        It also create the file if it does not exist.
    """
    filename = filename or os.environ.get(LOGGING_FILENAME_VAR)
    if not filename:
        return None
    with open(filename, "a+"):
        return filename

def get_logger(
                name=None,
                stash_config=None,
                filename=None,
                stdout_enabled=True,
                level=None
            ):
    logger = logging.getLogger(name or __name__)

    stdout_enabled = stdout_enabled and int(os.environ.get(LOGGING_STDOUT_ENABLED_VAR, 1))
    if stdout_enabled:
        stdout_formatter = get_formatter(stash_config=stash_config)
        stdout_handler = get_stdout_handler( formatter=stdout_formatter)
        logger.addHandler(stdout_handler)
    
    file = get_log_file(filename)
    if file:
        file_formatter = get_formatter(stash_config=stash_config)
        file_handler = get_file_handler(file, formatter=file_formatter)
        logger.addHandler(file_handler)

    level = level or int(os.environ.get(LOGGING_LEVEL_VAR, DEFAULT_LOGGING_LEVEL))
    logger.setLevel(level)
    return logger
