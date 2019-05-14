from sklearn.ensemble import GradientBoostingClassifier
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


class GradientBoost:
    def __init__(self):
        """
        Don't pass in anything
        """
        self.m = GradientBoostingClassifier()

    def log_loss_score(self, y_true, y_pred):
        """
        input:
            y_true, y_pred: 1d arrays of size n
        output:
            float: log loss score. It's a negative number, closer to zero is better.
        """
        return -log_loss(y_true, y_pred)

    def _change_data(self, old_df):
        #return jconvert(a_convert(old_df))
        """
        take dataframe, output dataframe
        """
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

    def optimize(self, param_grid, n_jobs = -1, cv = 5):
        """
        run grid search to change model
        """
        self.grid = GridSearchCV(self.m, param_grid = param_grid, cv = cv, n_jobs = n_jobs, scoring = 'neg_log_loss')
        self.grid.fit(self.X_train, self.y_train)
        self.m = self.grid.best_estimator_

    def score(self):
        return self.log_loss_score(self.y_test, self.m.predict_proba(self.X_test))

    def predict(self, df):
        X = self._change_data(df).values
        return self.m.predict(X)

    def predict_proba(self, df):
        converted = self._change_data(df)
        default_col = pd.Series([0]*len(converted))
        for col in self.data.columns:
            if col not in converted.columns and col != 'fraud':
                converted[col] = default_col
        return self.m.predict_proba(converted.values)

if __name__ == '__main__':
    data = pd.read_json('data/data.json')
    f = GradientBoost()
    f.fit(data)
    fail = data.drop('acct_type', axis = 1)
    #with open('modelg.p', 'wb') as file:
    #    pickle.dump(f, file)
