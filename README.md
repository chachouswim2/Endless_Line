# Eleven Hackathon Project - The Endless Line

## Project Title

Waiting Time Forecast for Theme Park Attractions

## Description

The goal of this project is to accurately forecast waiting times for attractions at a global theme park, E. has been experiencing a significant increase in waiting times since the pre-COVID era, which has affected visitor satisfaction. The objective is to use historical waiting time data, park attendance, weather data, parade schedules, and attraction opening/closing times to make medium/long term forecasts and improve the park's key performance indicators (KPIs).

## Model Optimization and Evaluation
The model is optimized using RMSE (root mean squared error) and also evaluated using the MAE (mean absolute error) for more interpretability.
The RMSE has been chosen to penalize outliers (avoid predicting waiting times that are very different from actuals) and ensure the error is scale dependent (ie. a 20% error for a 2h waiting time has more impact than a 20% error on a 10min waiting time). In future versions, we hope to create a custom loss that would also penalize underestimation more than overestimation since the main objective is first and foremost providing visitors with more visibility over the potential waiting times.

## Getting started with the repository
​
To ensure that all libraries are installed pip install the requirements file:
 
```pip install -r requirements.txt```

​
To run the model go to the console and run following command: 
 
```python main.py```

​
You should be at the source of the repository structure (ie. endlessline_eleven) when running the command.

Our repository is structured in the following way:
​
```
|endlessline_eleven
   |--data
   |--app
   |-----pages
   |--------features
   |-----home.py
   |-----requirements.txt
   |-----Pipfile
   |--output
   |--params
   |--src
   |-----evaluation
   |-----inference
   |-----load_merge_
   |-----model
   |-----preprocess
   |-----train
   |-----train_test_data
   |-----utils
   |--main.py
   |--README.md
   |--requirements.txt
   |--.gitignore
```

### data 

To properly get the data, one has to download it locally on his/her computer, unzip and put the folder in the repository. One should have a folder like data/ with 6 different elements:
- attendance.csv
- entity_merged.csv
- link_attraction_park.csv
- parade_night_show.xlsx
- waiting_times.csv
- weather_data.csv

In addition for the Web App utilisation, one should have two extra files:
- input_processed_data.csv: the output dataframe of the load_merge and preprocess .py files saved as csv used as input to the model to make predictions within the app.
- data_merged.csv: the merged inputs dataframe used within the app dashboard for KPIs tracking.

### output
The output folder contains three folders:
1) inference: containing the saved predictions provided by the inference class in the inference folder.
2) model: containing the saved trained pipeline in a .pkl file.
3) visualizations: containing the feature importance graphs and the effect of parameters on the performance metric when running a GridSearchCV (in the train.py file, calling the find_best_params function).

### src
The src folder contains all the different classes combined in the main.py file. The following is a description of all classes used.

1) load_merge
The load_merge class is used to load the different daa inputs and merge them into one input dataframe.

2) preprocess
The preprocess class is used to clean the data and add features such as temporal features, features modeling the real-time attendance, the time proximity with parades and night show and the impact of weather.

3) train_test_data
The train_test_data class is used to split into train and test data to evaluate our model on unseen data. The data is first sorted to avoid having leakage of past data in the test set.

4) model
The model class is used to create the model architecture and pipeline. The parameters of the model are set in the config file.

5) train
The train class is used to:
- Train a the model with features set in the config or run a GridSearchCV to find the best parameters.
- Save a figure showing the feature importances  in the output/visualizations/ folder.
- If a GridSearchCV is run, save figures showing the impact of different parameters on the performance metric (RMSE) in the output/visualizations/ folder.
- Evaluate the predictions on the training set using MAE.

Note: you can set the "train" field in the config file to true to train a model or set the gridsearch to true to run a gridsearchsv. If both are set to False, a pre-trained model is loaded (the name of the model should be added in the main.py file).

6) inference
The inference class is used to make predictions on the test set, save them and evaluate them using RMSE and MAE.

7) utils
The utils.py file is used to store utils functions. Currently, only the function initiating the logger is available.

### params
Params folder includes the configuration file and a logs.log file that is added to view the log info and debug

### app
Folder containing the file to create a web app that integrates the model and its predictions.

**Instructions to reproduce the environment and run the app locally:**

- Create a new environment:

```pipenv shell```

- Install requirements:

```pip install -r requirements.txt```

- Launch the app:

```streamlit run Home.py```

## Contacts LinkedIn 
​
If you have any feedback, please reach out to us on LinkedIn!
​
- [Inès Benito](https://www.linkedin.com/in/ines-benito/)
- [Lea Chader](https://www.linkedin.com/in/lea-chader/)
- [Rémi Khellaf](https://www.linkedin.com/in/remi-khellaf/)
- [Salah Mahmoudi](https://www.linkedin.com/in/salahmahmoudi/)
- [Charlotte Simon](https://www.linkedin.com/in/charlottesmn/)
