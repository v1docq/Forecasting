import glob
import json
import numpy as np
import pandas as pd
from core.train_script import FedotModel
from parser_utils.parser_module import enconde_heroes, open_file


def get_prediction(match_id):
    file_path = f'./current_match/{match_id}.json'
    save_path = f'./current_match/{match_id}.csv'
    df_encoded = open_file(file_path, path_to_save=save_path)
    df_model_features = df_encoded.values
    if 'Unnamed: 0' in df_encoded.columns:
        del df_encoded['Unnamed: 0']
    key = None
    model_time_segment = None
    model_path = None

    model_dict = {'0': r'.\models\0-10\pipeline\pipeline.json',
                  '1': r'.\models\5-15\pipeline\pipeline.json',
                  '2': r'.\models\15-25\pipeline\pipeline.json',
                  '3': r'.\models\30\pipeline\pipeline.json'}

    responce_dict = {
        "winner": "dire",
        "dire_win_probability": "67%",
        "radiant_win_probability": "33%",
        "time": "10:30"
    }
    model_time_segment = df_encoded['time'].values[0]
    if model_time_segment < 5:
        key = '0'
    elif 5 < model_time_segment < 15:
        key = '1'
    elif 15 < model_time_segment < 25:
        key = '2'
    else:
        key = '3'
    model_path = model_dict[key]

    clf_model = FedotModel(x_data=df_model_features, y_data=[], time=30)
    clf_model.fedot_model.load(model_path)
    predictions = clf_model.evalutate(x_test=df_model_features)[0]
    final_result = predictions[0] * 100

    if final_result > 50:
        winner = 'dire'
    else:
        winner = 'radiant'

    responce_dict['winner'] = winner
    responce_dict['dire_win_probability'] = f'{np.round(final_result)} %'
    responce_dict['radiant_win_probability'] = f'{np.round(100 - final_result)} %'
    responce_dict["time"] = model_time_segment

    return responce_dict
#
#
# if __name__ == '__main__':
#
#     get_prediction(df_encoded)