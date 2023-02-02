"""Make predictions, save them and get evaluation metric."""

import logging
import time
import warnings
import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

warnings.filterwarnings("ignore")
logger = logging.getLogger("main_logger")

class Inference():
    """Make predictions, save them and get evaluation metric."""
    def __init__(self, conf, pipeline,
                 X_test, y_test, split_class):
        self.conf = conf
        self.pipeline = pipeline
        self.X_test = X_test
        self.y_test = y_test
        self.split_class = split_class
    
    def eval_metric(self, y_pred):
        """Get evaluation metrics.
        Args:
            y_pred: predictions on test set.
        Returns:
            y_pred: the predictions from the test input.
        """
        rmse = mean_squared_error(self.y_test, y_pred, squared=False)
        mae = mean_absolute_error(self.y_test, y_pred)
        logger.info(f"The RMSE on test set is: {rmse:.2f}")
        logger.info(f"The MAE on test set is: {mae:.2f}")
        return rmse, mae
    
    def save_preds(self, y_pred):
        """Save predictions in csv file.
        Args:
            y_pred: predictions on test set.
        Returns:
            None
        """
        output_path = self.conf["paths"]["output_folder"]
        inference = self.conf["paths"]["inference"]
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        dates = self.split_class.get_test_data_dates()
        predictions_df = pd.DataFrame(data={"DEB_TIME": dates, "WAIT_TIME_MAX": y_pred})
        predictions_df.to_csv(output_path + inference +
                              "predictions" + timestamp + ".csv")
        return None
    
    def make_predictions(self):
        """Make predictions, save them and evaluate.
        Args:
            pipeline: the fitted pipeline.
            X_test: the test set inputs.
        Returns:
            y_pred: the predictions from the test input.
            rmse, mae: evaluation metrics
        """
        y_pred = self.pipeline.predict(self.X_test)
        rmse, mae = self.eval_metric(y_pred)
        self.save_preds(y_pred)
        return y_pred, rmse, mae
