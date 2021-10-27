from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb

class ModelSelection:
    def hyperparameter_tuning_xgboost(self, x_train, y_train):
        self.params = {
            "n_estimators": range(10, 30, 5),
            "criterion": ['gini', 'entropy'],
            "max_depth": range(2, 5, 1)
        }
        self.grid= GridSearchCV(xgb.XGBClassifier(), self.params, cv=5) 
        self.grid.fit(x_train, y_train)
        self.criterion = self.grid.best_params_['criterion']
        self.max_depth = self.grid.best_params_['max_depth']
        self.n_estimators = self.grid.best_params_['n_estimators']
        self.model_xgb = xgb.XGBClassifier(criterion=self.criterion, max_depth=self.max_depth, n_estimators=self.n_estimators, n_jobs=-1)
        self.model_xgb.fit(x_train, y_train)
        return self.model_xgb
    
    def hyperparameter_tuning_random_forest(self, x_train, y_train):
        self.params = {
            "n_estimators": range(10, 30, 5)
        }
        self.grid= GridSearchCV(RandomForestClassifier(), self.params, cv=5) 
        self.grid.fit(x_train, y_train)
        self.n_estimators = self.grid.best_params_['n_estimators']
        self.model_rf = RandomForestClassifier(n_estimators=self.n_estimators, n_jobs=-1)
        self.model_rf.fit(x_train, y_train)
        return self.model_rf

    def get_best_model(self, x_train, y_train, x_test, y_test):
        self.model_xgb = self.hyperparameter_tuning_xgboost(x_train, y_train)
        self.prediction_xgb = self.model_xgb.predict(x_test)
        self.score_xgb = self.model_xgb.score(x_test, y_test)

        self.model_rf = self.hyperparameter_tuning_random_forest(x_train, y_train)
        self.prediction_rf = self.model_rf.predict(x_test)
        self.score_rf = self.model_rf.score(x_test, y_test)

        if self.score_rf > self.score_xgb:
            return self.model_xgb, 'RANDOMFOREST', self.score_xgb
        else:
            return self.model_rf, 'XGBOOST', self.score_xgb
