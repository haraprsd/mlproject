import os
import sys
from source.mlproject.expection import CustomException
from source.mlproject.logger import logging
import pandas as pd
import numpy as np
import pickle

def save_pickle_object(filename, obj):
    try:
        dir_path = os.path.dirname(filename)
        os.makedirs(dir_path, exist_ok=True)

        with open(filename, "wb") as file_obj:
            pickle.dump(obj, file_obj)
            
    except Exception as e:
        raise CustomException (e, sys)

