from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
#from max_pipeline import max_data_pipeline
from eda_alex import a_convert
from eda_john import jconvert
from max_pipeline import max_data_pipeline
from main import do_it
from sklearn.metrics import log_loss, make_scorer


class FraudLogit:
    def __init__(self, data = None):
        """
        can pass in data or nothing
        """
        if data:
            self.data = self._change_data()
            self.X = self.data.drop(['fraud'], axis = 1).values
            self.y = self.data['fraud'].values
        self.m = RandomForestClassifier()
        self.scorer = (lambda y_true,y_pred: -log_loss(y_true,y_pred))

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
        
        self.X = self.data.drop(['fraud'], axis = 1).values
        self.y = self.data['fraud'].values
        self.m.fit(self.X,self.y)

    def optimize(self, param_grid, n_jobs = 5):
        """
        run grid search to change model
        """
        self.grid = GridSearchCV(self.m, param_grid = param_grid, n_jobs = n_jobs, scoring = make_scorer(self.scorer))
        self.grid.fit(self.X, self.y)
        self.m = self.grid.best_estimator_

    def predict(self, X_test):
        """
        just pass the prediction to sklearn's model, encoded inside
        """
        return self.m.predict(X_test)

    def predict_df(self, df):
        X = self._change_data(df).values
        return self.m.predict(X)

    def predict_proba(self, X_test):
        return self.m.predict_proba(X_test)

    def score(self, X_test, y_test):
        return self.scorer(y_test, self.m.predict(X_test))