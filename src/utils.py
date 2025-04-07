import os
import sys

import numpy as np
import pandas as pd
import dill

from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException
from src.logger import logging

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise CustomException(e, sys)
    
def evaluate_models(X_train, y_train, X_test, y_test, models, params, cv=3, n_jobs=-1, verbose=1):
    try:
        report = {}

        for name, model in models.items():
            logging.info(f"🔍 Tuning hyperparameters for {name}...")
            param_grid = params.get(name, {})

            # If hyperparameters are defined, use GridSearchCV
            if param_grid:
                grid_search = GridSearchCV(estimator=model,
                                           param_grid=param_grid,
                                           cv=cv,
                                           n_jobs=n_jobs,
                                           verbose=verbose,
                                           scoring='r2',
                                           refit=True)
                grid_search.fit(X_train, y_train)
                best_model = grid_search.best_estimator_
                best_params = grid_search.best_params_
            else:
                best_model = model
                best_model.fit(X_train, y_train)
                best_params = {}

            # Predictions
            y_train_pred = best_model.predict(X_train)
            y_test_pred = best_model.predict(X_test)

            # R2 Scores
            train_r2 = r2_score(y_train, y_train_pred)
            test_r2 = r2_score(y_test, y_test_pred)

            report[name] = {
                "Train R2 Score": train_r2,
                "Test R2 Score": test_r2,
                "Best Parameters": best_params
            }

        return report

    except Exception as e:
        raise CustomException(e,sys)