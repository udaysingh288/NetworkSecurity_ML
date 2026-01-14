import yaml
import os,sys
from networksecurity.exception.exception import NetworkSecurityException
import sys
import pickle


def read_yaml_file(file_path: str) -> dict:
    """Reads a YAML file and returns its contents as a dictionary.

    Args:
        file_path (str): The path to the YAML file.
    Returns:
        dict: The contents of the YAML file as a dictionary.
    """

    with open(file_path, 'r') as file:
        return yaml.safe_load(file)     

def write_yaml_file(file_path: str, content: dict, replace: bool = False) -> None:
    """Writes a dictionary to a YAML file.

    Args:
        file_path (str): The path to the YAML file.
        content (dict): The dictionary to write to the YAML file.
    """
    try:
        if not replace and os.path.exists(file_path):
            raise FileExistsError(f"File {file_path} already exists. Use replace=True to overwrite.")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(content, file)    
    except Exception as e:
        raise NetworkSecurityException(e, sys)

