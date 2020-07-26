"""
utils
"""

from __future__ import annotations
import logging.config
import logging
import os
import functools
import json
import datetime

import yaml

from src import exception


_LOGGER = logging.getLogger(__name__)


CONFIG_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "data", "configuration", "{env_alias}.yml",
)


def configure_logging(configuration: dict) -> None:
    log_dict_config = configuration["log"]
    for handler_alias, handler_config in log_dict_config["handlers"].items():
        if "filename" in handler_config.keys():
            log_file_path = os.path.join(
                os.path.dirname(__file__),
                "..",
                "data",
                "log",
                handler_config["filename"],
            )
            if not os.path.exists(log_file_path):
                with open(log_file_path, "w"):
                    pass

            handler_config["filename"] = log_file_path

    logging.config.dictConfig(log_dict_config)
    _LOGGER.debug(f"configured logging")


def load_configuration(env_alias: str) -> dict:
    config_file_path = CONFIG_FILE_PATH.format(env_alias=env_alias)
    with open(config_file_path) as fh:
        return yaml.load(fh, Loader=yaml.FullLoader)


def write_configuration(env_alias: str, config_dict: dict) -> None:
    config_file_path = CONFIG_FILE_PATH.format(env_alias=env_alias)
    with open(config_file_path, "w") as fh:
        yaml.dump(config_dict, fh, default_flow_style=False)


def config_env(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        env_alias = kwargs.get("env")
        if not env_alias:
            raise exception.BoxTypeError("Missing 'env' kwargs")

        config = load_configuration(env_alias)
        configure_logging(config)
        _LOGGER.info(f"Running {func.__name__} CLI")
        kwargs["config"] = config

        return func(*args, **kwargs)

    return wrapper


def load_mock_event():
    with open(
        os.path.join(os.path.dirname(__file__), "..", "data", "mock", "event.json"), "r"
    ) as fh:
        event_dict = json.load(fh)

    event_dict["created_at"] = datetime.datetime.now()

    return event_dict
