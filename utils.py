import json
import logging
import pandas as pd

class Params():
    """
    Class that loads parameters from a json file

    Example:
    ```
    params = Params(json_path)
    print(params.file_type)
    params.file_type = "10-Q" # change the value of file_type to 10-Q
    ```
    """

    def __init__(self, json_path):
        self.update(json_path)

    def update(self, json_path):
        with open(json_path) as f:
            param = json.load(f)
            self.__dict__.update(param)

    @property
    def dict(self):
        """Gives dict-like access to Params instance by `params.dict["file_type"]`"""
        return self.__dict__

def setlogger(log_path):
    """

    """

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(stream_handler)

def get_cik_list(data_path):
    """
    """

    data = pd.read_csv(data_path, delimiter="|", dtype={"CIK": str})

    return data["CIK"].tolist()
