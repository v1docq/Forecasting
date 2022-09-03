import glob
import json
import numpy as np
import pandas as pd
from core.train_script import FedotModel
from parser_utils.parser_module import enconde_heroes, open_file


def get_prediction(match_id):
    file_path = f'./current_match/{match_id}.json'
    save_path = f'./current_match/{match_id}.csv'
    list_of_df = open_file(file_path, path_to_save=f'./current_match/{match_id}.csv')
    # files = glob.glob(save_path)
    # df_encoded = pd.concat([pd.read_csv(f) for f in files], axis=0)
    df_encoded = pd.read_csv(save_path)
    df_model_features = df_encoded.values
    df_model_class_labels = []
    match_id = df_encoded['match_id'].values[0]
    del df_encoded['Unnamed: 0']
    del df_encoded['match_id']
    key = None
    model_time_segment = None
    model_path = None

    model_dict = {'0': r'.\models\0-10\pipeline\pipeline.json',
                  '1': r'.\models\10-20\pipeline\pipeline.json',
                  '2': r'.\models\20-30\pipeline\pipeline.json',
                  '3': r'.\models\30\pipeline\pipeline.json'}

    responce_dict = {
        "winner": "dire",
        "dire_win_probability": "67%",
        "radiant_win_probability": "33%",
        "time": "10:30"
    }
    model_time_segment = df_encoded['time'].values[0]
    if model_time_segment < 10:
        key = '0'
    elif 10 < model_time_segment < 20:
        key = '1'
    elif 20 < model_time_segment < 30:
        key = '2'
    else:
        key = '3'
    model_path = model_dict[key]

    clf_model = FedotModel(x_data=df_model_features, y_data=df_model_class_labels, time=30)
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
    # with open('./current_match/prediction.json', 'w') as f:
    #     json.dump(responce_dict, f)

    return responce_dict
#
#
# if __name__ == '__main__':
#
#     get_prediction(df_encoded)
