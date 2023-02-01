"""Train model and get best params."""

import logging
import time
import warnings
import joblib
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.model_selection import GridSearchCV
from xgboost import XGBRegressor

warnings.filterwarnings("ignore")
logger = logging.getLogger("main_logger")

class Train():
    """Train model."""
    def __init__(self, conf, X_train, y_train):
        self.conf = conf
        self.X_train = X_train
        self.y_train = y_train
    
    def train_model(self, pipeline):
        """Train model using cross validation split.
        Args:
            pipeline: model pipeline.
            X_train: training inputs.
            y_train: training target variable.
        Returns:
            scores: prints the scores of each validation.
            mean and std of scores: prints the mean and std of the scores.
        """
        cv = TimeSeriesSplit(n_splits=5)
        scores = cross_val_score(pipeline, self.X_train, self.y_train,
                                cv=cv, scoring='neg_root_mean_squared_error')
        logger.info(f'RMSE: {scores}')
        logger.info(f'RMSE (all folds): {-scores.mean():.3} ± {(-scores).std():.3}')
        pipeline.fit(self.X_train, self.y_train)
        return pipeline
    
    def save_model(self, pipeline):
        """Save model."""
        path = self.conf["paths"]["output_folder"]
        model_folder = self.conf["paths"]["model"]
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        full_path = path + model_folder + "pipeline" + timestamp
        joblib.dump(pipeline, full_path + ".pkl")
        return None
    
    def load_model(self, pipeline_name):
        """Load and return model."""
        path = self.conf["paths"]["output_folder"]
        model_folder = self.conf["paths"]["model"]
        full_path = path + model_folder + pipeline_name
        pipeline = joblib.load(full_path + '.pkl')
        return pipeline

    def find_best_params(self, pipeline):
        """Do a grid search to find the best params.
        Args:
            pipeline: model pipeline.
            X_train: training inputs.
            y_train: training target variable.
        Returns:
            the best params.
        """
        param_grid = {
            'model__max_depth': [2, 3, 5, 7, 10],
            'model__n_estimators': [10, 100, 500],
            'model__learning_rate': [0.1, 0.05, 0.01],
            'model__min_child_weight': [2, 4, 6],
            'model__reg_lambda': [1e-5, 1e-2, 0.1, 1, 100]}
        cv = TimeSeriesSplit(n_splits=5)
        grid = GridSearchCV(self.pipeline, param_grid, cv=cv,
                            n_jobs=-1, scoring='neg_root_mean_squared_error')
        
        mean_score = grid.cv_results_["mean_test_score"][grid.best_index_]
        std_score = grid.cv_results_["std_test_score"][grid.best_index_]
        pipeline = grid.best_estimator_
        logger.info(f"Best parameters: {grid.best_params_}")
        logger.info(f"Best Estimator: {grid.best_estimator_}")
        logger.info(f"Mean CV score: {mean_score: .6f}")
        logger.info(f"Standard deviation of CV score: {std_score: .6f}")
        pipeline.fit(self.X_train, self.y_train)
        return pipeline