"""Get the training and test data."""

from sklearn.model_selection import train_test_split

class TrainTest():
    """Create the model architecture."""
    def __init__(self, conf, data):
        self.conf = conf
        # sort the data by time so we ensure that the validation set in the split does not contain past data
        self.data = data.sort_values(by="DEB_TIME")
    
    def train_test_split(self):
        """Split the data into train and test set.
        Args:
            data: dataframe including all inputs and target.
        Returns:
            X_train, X_valid: the inputs for the train and validation set.
            y_test, y_test: the target variable for the train and test set.
        """
        X = self.data.drop(['WAIT_TIME_MAX', "DEB_TIME"], axis=1)
        y = self.data["WAIT_TIME_MAX"]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,train_size=0.8, test_size=0.2, random_state=0)
        return X_train, X_test, y_train, y_test