# Eleven Hackathon- The Endless Line

## Data 

To properly get the data, one has to download it locally on his/her computer, unzip and put the folder in the main folder. One should have a folder like data/ with 6 different elements:
- attendance.csv
- entity_merged.csv
- link_attraction_park.csv
- parade_night_show.xlsx
- waiting_times.csv
- weather_data.csv
After running the different building data functions, one should have two extra files:
- input_processed_data.csv
- data_merged.csv

## Repository description

### src
Folder containing the python files to create the different models and associated train/test data.

### params
Folder containing the ,json configuration file for the model training.

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
