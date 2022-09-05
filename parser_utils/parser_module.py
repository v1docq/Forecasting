import numpy as np
import pandas as pd
import glob
import json


def open_file(file_path, path_to_save):
    tmp = []
    json_df = pd.read_json(file_path)
    for idx, row in json_df.iterrows():
        data = pd.DataFrame.from_dict(row.values[0])
        heroes_dict = data['teams'].values
        data['time'] = data['time'].astype(int)
        data['networth'] = data['networth'].astype(int)
        data['time'] = data['time'] / 60
        data['time'] = data['time'].apply(lambda x: np.round(x, decimals=2))
        data['tower_radiant'] = data['tower_radiant'].apply(lambda x: x.count('0'))
        data['tower_dire'] = data['tower_dire'].apply(lambda x: x.count('0'))
        if data['advantage'].values[0] == 'radiant':
            data['networth'].values[0] = -data['networth'].values[0]
        del data['teams']
        for val in heroes_dict:
            heroes = pd.DataFrame.from_dict(val, orient='index').T
            side = heroes.iloc[:1, :1].values[0][0]
            del heroes['type']
            heroes.columns = [f'{x}_{side}' for x in heroes.columns]
            data = pd.concat([data, heroes], axis=1)
        tmp.append(data.iloc[:1, :])
    final_df = pd.concat(tmp)
    final_df = final_df.sort_values(by=['time'])
    if 'winner' in final_df.columns:
        final_df['label'] = [1 if x == 'dire' else 0 for x in final_df['winner'].values]
        del final_df['winner']

    del final_df['advantage']
    return final_df


def open_file_for_train(file_path, path_to_save):
    files = glob.glob(file_path)
    list_of_df = []
    count = 0
    for f in files:
        try:
            tmp = []
            json_df = pd.read_json(f)
            count += 1
            for idx, row in json_df.iterrows():
                data = pd.DataFrame.from_dict(row.values[0])
                heroes_dict = data['teams'].values
                data['time'] =data['time'].astype(int)
                data['networth'] = data['networth'].astype(int)
                data['time'] = data['time'] / 60
                data['time'] = data['time'].apply(lambda x: np.round(x, decimals=2))
                data['tower_radiant'] = data['tower_radiant'].apply(lambda x: x.count('0'))
                data['tower_dire'] = data['tower_dire'].apply(lambda x: x.count('0'))
                if data['advantage'].values[0] == 'radiant':
                    data['networth'].values[0] = -data['networth'].values[0]
                del data['teams']
                for val in heroes_dict:
                    heroes = pd.DataFrame.from_dict(val, orient='index').T
                    side = heroes.iloc[:1, :1].values[0][0]
                    del heroes['type']
                    heroes.columns = [f'{x}_{side}' for x in heroes.columns]
                    data = pd.concat([data, heroes], axis=1)
                tmp.append(data.iloc[:1, :])
            final_df = pd.concat(tmp)
            final_df = final_df.sort_values(by=['time'])
            if 'winner' in final_df.columns:
                final_df['label'] = [1 if x=='dire' else 0 for x in final_df['winner'].values]
                del final_df['winner']

            final_df['match_id'] = f
            del final_df['advantage']
            final_df.to_csv(f'./{path_to_save}/{count}.csv')
            list_of_df.append(final_df)
        except Exception as ex:
            print(f'Error-{ex}')
    return list_of_df



def enconde_heroes(df: pd.DataFrame):
    sss = []
    for i in range(len(df.iloc[:, 3:25].values)):
        for j in range(0, 22, 1):
            sss.append(df.iloc[:, 3:25].values[i][j])
    list_of_heroes = sss
    list_of_heroes = set(list_of_heroes)

    list_of_teams = []
    for i, j in zip(df[' First Pick'].unique(), df[' Second Pick'].unique()):
        list_of_teams.append(i)
        list_of_teams.append(j)
    list_of_teams = set(list_of_teams)

    list_of_сlasses = []
    for i in df['Winner'].unique():
        list_of_сlasses.append(i)
    list_of_сlasses = set(list_of_сlasses)

    dct_сlasses = dict(zip(list_of_сlasses, range(len(list_of_сlasses))))
    dct_heroes = dict(zip(list_of_heroes, range(len(list_of_heroes))))
    dct_teams = dict(zip(list_of_teams, range(len(list_of_teams))))
