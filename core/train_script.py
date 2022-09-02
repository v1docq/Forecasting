from fedot.api.main import Fedot
from sklearn.metrics import roc_auc_score as roc_auc


class FedotModel:
    def __init__(self, x_data, y_data, time):
        self.fedot_model = Fedot(problem='classification',
                                 timeout=time,
                                 pop_size=10,
                                 num_of_generations=10,
                                 seed=42, logging_level=20,
                                 safe_mode=False)
        self.x_data = x_data
        self.y_data = y_data

    def run_model(self):

        # During fit, the pipeline composition algorithm is started
        self.fedot_model.fit(features=self.x_data,
                             target=self.y_data)

    def evalutate(self, x_test):
        return self.fedot_model.predict_proba(features=x_test)

    def get_metrics(self):
        prediction = self.fedot_model.predict_proba(features=self.x_data)
        print(self.fedot_model)
        print(f'ROC AUC score on training sample: {roc_auc(self.y_data, prediction):.3f}')
