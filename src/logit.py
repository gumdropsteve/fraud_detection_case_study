from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
#from max_pipeline import max_data_pipeline
from eda_alex import a_convert
from eda_john import jconvert
from max_pipeline import max_data_pipeline
from main import do_it
from sklearn.metrics import log_loss
from sklearn.metrics import make_scorer
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle


class FraudLogit:
    def __init__(self):
        """
        can pass in data or nothing
        """
        self.m = LogisticRegression()

    def log_loss_score(self, y_true, y_pred):
        return -log_loss(y_true, y_pred)

    def _change_data(self, old_df):
        #return jconvert(a_convert(old_df))
        return max_data_pipeline(jconvert(a_convert(do_it(old_df))))

    def fit(self, data):
        """
        data is a dataframe
        no output
        """


        self.data = self._change_data(data)

        self.X = self.data.drop(['fraud'], axis = 1).values
        self.y = self.data['fraud'].values

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y)
        self.m.fit(self.X_train,self.y_train)

    def optimize(self, param_grid, n_jobs = 5):
        """
        run grid search to change model
        """
        self.grid = GridSearchCV(self.m, param_grid = param_grid, n_jobs = n_jobs, scoring = make_scorer(self.log_loss_score))
        self.grid.fit(self.X_train, self.y_train)
        self.m = self.grid.best_estimator_

    def score(self):
        return self.log_loss_score(self.y_test, self.m.predict_proba(self.X_test))

    def predict(self, df):
        X = self._change_data(df).values
        return self.m.predict(X)

    def predict_proba(self, df):
        X = self._change_data(df).values
        return self.m.predict_proba(X)

if __name__ == '__main__':
    data = pd.read_json('data/data.json')
    f = FraudLogit()
    f.fit(data)
    fail = data.drop('acct_type', axis = 1)

    with open('model.p', 'wb') as file:
        pickle.dump(f, file)
