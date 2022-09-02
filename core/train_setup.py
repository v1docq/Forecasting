# from sklearn.model_selection import train_test_split
# from collections import Counter
# import model_evaluation_utils as meu
# from sklearn.model_selection import GridSearchCV
#
#
# df_model = df.copy()
# col_to_drop = [' First Pick',' Second Pick']
# df_model = df_model.drop(col_to_drop, axis=1)
# df_model = df_model.fillna(0)
#
# df_model_features = df_model.iloc[:,1:23]
# df_model_names = df_model.columns[1:23]
# df_model_class_labels = np.array(df_model['Winner'])
#
# df_model_train_X, df_model_test_X, df_model_train_y, df_model_test_y = train_test_split(df_model_features, df_model_class_labels,
#                                                                     test_size=0.2, random_state=42)
#
# print(Counter(df_model_train_y), Counter(df_model_test_y))
# print('Features:', list(df_model_names))
#
# from sklearn.preprocessing import StandardScaler
# df_model_ss = StandardScaler().fit(df_model_train_X)
# df_model_train_SX = df_model_ss.transform(df_model_train_X)
# df_model_test_SX = df_model_ss.transform(df_model_test_X)
#
# from sklearn.preprocessing import LabelEncoder
# le = LabelEncoder()
# df_model_class_labels = le.fit_transform(df_model_class_labels)
#
#
# from sklearn.preprocessing import StandardScaler
# df_model_ss = StandardScaler().fit(df_model_train_X)
# df_model_train_SX = df_model_ss.transform(df_model_train_X)
# df_model_test_SX = df_model_ss.transform(df_model_test_X)
#
# from sklearn.preprocessing import LabelEncoder
# le = LabelEncoder()
# df_model_class_labels = le.fit_transform(df_model_class_labels)
#
#
# from sklearn.decomposition import PCA
# # feature extraction
# pca = PCA(n_components=10)
# fit = pca.fit(df_model_train_SX)