"""Create model structure."""

import logging
import xgboost
import warnings
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")
logger = logging.getLogger("main_logger")

class Model():
    """Create the model architecture."""
    def __init__(self, conf):
        self.conf = conf
    
    def define_model_pipeline(self):
        """Define model pipeline.
        Args:
            None.
        Return:
            XGBoost model pipeline.
        """
        numerical_cols = self.conf["model"]["numerical_cols"]
        categorical_cols = self.conf["model"]["categorical_cols"]
        passthrough_cols = self.conf["model"]["passthrough_cols"]
        numerical_transformer = StandardScaler()
        categorical_transformer = OneHotEncoder(handle_unknown='ignore')

        preprocessor = ColumnTransformer(transformers=[
            ('num', numerical_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols),
            ('pass', 'passthrough', passthrough_cols)
            ],
            remainder= "drop")
        n_estimators = self.conf["model"]["n_estimators"]
        max_depth = self.conf["model"]["max_depth"]
        min_child_weight = self.conf["model"]["min_child_weight"]
        reg_lambda = self.conf["model"]["reg_lambda"]
        learning_rate = self.conf["model"]["learning_rate"]
        model = XGBRegressor(n_estimators=n_estimators, max_depth=max_depth,
                            min_child_weight=min_child_weight, reg_lambda=reg_lambda,
                            learning_rate=learning_rate, random_state=0, tree_method = "gpu_hist")

        my_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                              ('model', model)
                             ])
        return my_pipeline
     

