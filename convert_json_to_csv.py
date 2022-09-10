from parser_utils.parser_module import *

if __name__ == '__main__':
    file_path = './historyData/*.json'
    save_path = 'Encoded_data/732/'
    list_of_df = open_file_for_train(file_path,save_path)

