"""Main script to run src."""

import json
import random
from time import time
from src.utils.utils import my_get_logger
from src.load_merge.load_merge import Load_Merge
from src.preprocess.preprocess import Preprocess
from src.model.model import Model
from src.train.train import Train
from src.train_test_data.train_test_split import TrainTest
from src.inference.inference import Inference

random.seed(0)

def main(logger, conf):
    """
    Main function launching step by step the pipeline.
    Args:
        logger: logger file.
        conf: config file.
    """
    START = time()
    load_class = Load_Merge(conf)
    df = load_class.get_full_input()
    preprocess_class = Preprocess(conf, df)
    df = preprocess_class.create_final_input()
    time_1 = time()
    logger.debug(
        "Time to load and preprocess data:" + str(time_1 - START)
    )
    split_class = TrainTest(conf, df)
    X_train, X_test, y_train, y_test = split_class.train_test_split()
    train_class = Train(conf, X_train, y_train)
    model_class = Model(conf)
    if conf["model"]["train"]:
        pipeline = model_class.define_model_pipeline()
        pipeline_fit = train_class.train_model(pipeline)
        train_class.save_model(pipeline_fit)
        time_2 = time()
        logger.debug(
            "Time to train a model:" + str(time_2 - time_1)
        )
    elif conf["model"]["gridsearch"]:
        pipeline = model_class.define_model_pipeline()
        pipeline_fit = train_class.find_best_params(pipeline)
        train_class.save_model(pipeline_fit)
        time_2 = time()
        logger.debug(
            "Time to find the best model with gridsearch and train it:" + str(time_2 - time_1)
        )
    else:
        pipeline_fit = train_class.load_model("pipeline20230202-092805")
        time_2 = time()
        logger.debug(
            "Time to load a saved model:" + str(time_2 - time_1)
        )
    mae = train_class.evaluation_train(pipeline_fit)
    inference_class = Inference(conf, pipeline_fit, X_test, y_test, split_class)
    y_pred, rmse, mae = inference_class.make_predictions()
    time_3 = time()
    logger.debug(
            "Time to make and save predictions:" + str(time_3 - time_2)
        )

    return None


if __name__ == "__main__":
    path_conf = "params/config.json"
    conf = json.load(open(path_conf, "r"))
    path_log = conf["path_log"]  # "../log/my_log_file.txt"
    log_level = conf["log_level"]  # "DEBUG"
    # instanciation of the logger
    logger = my_get_logger(path_log, log_level, my_name="main_logger")
    try:
        main(logger=logger, conf=conf)

    except Exception:
        logger.error("Error during execution", exc_info=True)
