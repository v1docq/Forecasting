import glob

import pandas as pd
from sklearn.model_selection import train_test_split
from core.train_script import FedotModel
from parser_utils.parser_module import enconde_heroes, open_file
from core.train_setup import *
from sklearn.metrics import roc_auc_score as roc_auc

model_dict = {0: r'.\models\0-10\pipeline\pipeline.json',
              10: r'.\models\10-20\pipeline\pipeline.json',
              20: r'.\models\20-30\pipeline\pipeline.json',
              30: r'.\models\30\pipeline\pipeline.json'}

if __name__ == '__main__':
    file_path = './Encoded_data/732/*.csv'
    train_mode = True
    start = 15
    end = 25
    model_path = fr'D:\РАБОТЫ РЕПОЗИТОРИИ\Репозитории\Forecasting\models\models\{start}-{end}\pipeline\pipeline.json'
    # list_of_df = open_file(path)
    files = glob.glob(file_path)

    df_encoded = pd.concat([pd.read_csv(f) for f in files], axis=0)
    del df_encoded['Unnamed: 0']
    del df_encoded['match_id']

    df_encoded = df_encoded[(df_encoded['time'] > start) & (df_encoded['time'] < end)]
    # df_encoded = df_encoded[(df_encoded['time'] > 20.0) & (df_encoded['time'] < 30.0)]
    df_model_class_labels = df_encoded['label'].values
    del df_encoded['label']

    df_model_features = df_encoded.values
    if train_mode:
        df_model_train_X, df_model_test_X, df_model_train_y, df_model_test_y = train_test_split(df_model_features,
                                                                                                df_model_class_labels,
                                                                                                test_size=0.2,
                                                                                                random_state=42)
        clf_model = FedotModel(x_data=df_model_train_X, y_data=df_model_train_y, time=60)
        clf_model.run_model()
        clf_model.get_metrics()
        predictions = clf_model.evalutate(x_test=df_model_test_X)
        final_result = roc_auc(df_model_test_y, predictions)
        clf_model.fedot_model.export_as_project()
    else:
        clf_model = FedotModel(x_data=df_model_features, y_data=df_model_class_labels, time=30)
        clf_model.fedot_model.load(model_path)
        predictions = clf_model.evalutate(x_test=df_model_features)
        final_result = roc_auc(df_model_class_labels, predictions)
        _ = 1
