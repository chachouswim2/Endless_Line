# Eleven Hackathon Project - The Endless Line

## Project Title

Waiting Time Forecast for Theme Park Attractions

## Description

The goal of this project is to accurately forecast waiting times for attractions at a global theme park, E. With a significant increase in waiting times since the pre-COVID era, visitor satisfaction has been affected. The objective is to use historical waiting time data, park attendance, weather data, parade schedules, and attraction opening/closing times to make medium/long term forecasts and improve the park's key performance indicators (KPIs).


## Getting started with the repository
​
To ensure that all libraries are installed pip install the requirements file:
 
```
pip install -r requirements.txt
```
​
To run the model go to the console and run following command: 
 
```
python main.py
```
​
You should be at the source of the repository structure (ie. endlessline_eleven) when running the command.

Our repository is structured in the following way:
​
```
|endlessline_eleven
   |--data
   |--app
   |-----pages
   |-----home.py
   |-----requirements.txt
   |-----Pipfile
   |--features
   |--models
   |--notebooks
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

### Data 

To properly get the data, one has to download it locally on his/her computer, unzip and put the folder in the main folder. One should have a folder like data/ with 6 different elements:
- attendance.csv
- entity_merged.csv
- link_attraction_park.csv
- parade_night_show.xlsx
- waiting_times.csv
- weather_data.csv

In addition for the Web App utilisation, one should have two extra files:
- input_processed_data.csv
- data_merged.csv

### src
The src folder contains all the different classes combined in the main.py file. The following is a description of all classes used.

### params
Params folder includes the configuration file and a logs.log file that is added to view the log info and debug

### features
Folder containing the functions used for the streamlit plots and data building/cleaning.

### models
Folder containing the saved models as .pkl.

### notebooks
Folder containing the notebooks with templates.

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
