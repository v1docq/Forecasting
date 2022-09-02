import glob

import pandas as pd
from core.train_script import FedotModel
from parser_utils.parser_module import enconde_heroes, open_file

if __name__ == '__main__':
    file_path = './historyData/732/*.json'
    path_to_save = './Encoded_data/732/'
    list_of_df = open_file(file_path, path_to_save)
    _ = 1
