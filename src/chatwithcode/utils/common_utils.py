import os
import shutil
import json
import yaml
import torch
from pathlib import Path
from box.exceptions import BoxValueError
from box import ConfigBox
from ensure import ensure_annotations
from typing import Any
from datetime import datetime
import logging


def log(file_object:Path, log_message:str) -> None:
    """
        Logs a message to a file using the Python logging module.

        Args:
            file_object (str): The name of the file to log the message to.
            log_message (str): The message to be logged.

        Raises:
            ValueError: If file_object or log_message is None or empty.

        Returns:
            None
    """
    if not file_object or not log_message:
        raise ValueError('file_object and log_message cannot be None or empty')
    try:
        now = datetime.now()
        date = now.date()
        current_time = now.strftime("%H:%M:%S")
        
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger()

        file_handler = logging.FileHandler(filename=file_object)
        logger.addHandler(file_handler)
        logging.info(f'{date}\t{current_time}\t{log_message}')
        
    except Exception as e:
        raise e
    

@ensure_annotations
def read_params(config_path: Path) -> ConfigBox:
    """
        Read the YAML file at the specified path and return its contents as a dictionary.

        Args:
            config_path (str): The path to the YAML file.

        Returns:
            ConfigBox: ConfigBox type

        Raises:
            Exception: If there is an error while reading the file.
    """
    try:
        with open(config_path) as yaml_file:
            config = yaml.safe_load(yaml_file)
        return ConfigBox(config)
    
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as ex:
        raise ex


@ensure_annotations
def clean_prev_dirs_if_exis(dir_path: str):
    """
        Clean up a directory by removing it if it exists.

        Args:
            dir_path (str): The path to the directory that needs to be cleaned up.

        Returns:
            None

        Raises:
            Any exception that occurs during the removal process is caught and ignored.
    """
    try:
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path)
    except Exception as ex:
        raise ex


@ensure_annotations
def create_dir(dirs: list):
    """
        Create directories specified in a list.

        Args:
            dirs (list): A list of directory names to be created.

        Raises:
            Exception: If any exception occurs during the creation of directories.

        Example Usage:
            create_dir(['dir1', 'dir2'])
    """
    try:
        for dir in dirs:
            os.makedirs(dir, exist_ok=True)
    except Exception as e:
        raise e


# @ensure_annotations
def save_json_file(file_path: Path, report: dict):
    """
        Saves the report dictionary to a file in JSON format.

        Args:
            file_path (str): The path of the file where the report will be saved.
            report (dict): The report data that will be written to the file.

        Raises:
            Exception: If any error occurs during the file writing process.

        Example:
            save_report('report.json', {'name': 'John', 'age': 25})
    """
    try:
        with open(file_path, 'w') as f:
            json.dump(report, f, indent=4)
    except Exception as e:
        raise e


# @ensure_annotations
def load_json_file(file_path:Path) -> ConfigBox:
    """
        Load a report from a file and return a ConfigBox object.

        Args:
            file_path (Path): The path to the file containing the report.

        Returns:
            ConfigBox: A ConfigBox object representing the content of the file.

        Raises:
            Exception: If there is an error while loading the report.

        Example Usage:
            file_path = Path("report.json")
            report = load_report(file_path)
    """
    try:
        with open(file_path) as f:
            content = json.load(f)
        return ConfigBox(content)

    except Exception as ex:
        raise ex