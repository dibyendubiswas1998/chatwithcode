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


def insert_data_tojson_file(file_path:Path, data_dct:dict):
    try:
        if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    data = json.load(file)  # Load existing JSON data
        else:
            data = [] 
        data.append(data_dct) # append the data to json file
        with open(file_path, 'w') as file:
                json.dump(data, file, indent=4) 

    except Exception as e:
        raise e