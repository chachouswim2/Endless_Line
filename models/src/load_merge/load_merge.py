"""Load input dataframes and merge into one dataframe."""
import pandas as pd
import warnings
import logging

warnings.filterwarnings("ignore")
logger = logging.getLogger("main_logger")

warnings.filterwarnings("ignore")

class Load_Merge():
    """Load input dataframes and merge into one dataframe."""
    def __init__(self, conf):
        self.conf = conf
    
    def load_data(self):
        """ Load all the attendance, weather and waiting data

        Returns:
            attendance, entity_schedule, link_attraction, parade_night_show,
            waiting_times, weather_data: All dataframes returned by the function
        """
        
        logger.info('Data Loading...')
        input_path = self.conf["paths"]["input_folder"]
        attendance = self.conf["paths"]["attendance"]
        entity_schedule = self.conf["paths"]["entity_schedule"]
        link_attraction = self.conf["paths"]["link_attraction"]
        parade_night_show = self.conf["paths"]["parade_night_show"]
        waiting_times = self.conf["paths"]["waiting_times"]
        weather_data = self.conf["paths"]["weather_data"]

        attendance = pd.read_csv(input_path + attendance)
        entity_schedule = pd.read_csv(input_path + entity_schedule)
        link_attraction = pd.read_csv(input_path + link_attraction, sep=';')
        parade_night_show = pd.read_excel(input_path + parade_night_show)
        waiting_times = pd.read_csv(input_path + waiting_times)
        weather_data = pd.read_csv(input_path + weather_data)

        parade_night_show.drop(columns=['Unnamed: 0'], inplace=True)
        logger.info('Data Loaded!')

        return (attendance, entity_schedule, link_attraction,
                parade_night_show, waiting_times,
                weather_data)
        
    def sort_reset_date(self, df, col_d='WORK_DATE'):
        """ Sort and reset dataframes based on the date and time

        Args:
            df: dataframes containing column about the date
            col_d: date column of the dataframe, to be manipulated

        Returns:
            df: sorted dataframe with reset index
        """
        
        df.sort_values(by=col_d, inplace=True)
        df.reset_index(inplace=True, drop=True)
        
        return df

    def hour_rounder(self, df, col_t='DEB_TIME'):
        """ Floor down the time to the hour to merge on weather data

        Args:
            df: dataframe to be modified
            col_t: column to be used for floor the time

        Returns:
            df: updated dataframe with new time floored to the hour
        """

        df['TIME_HOUR'] = pd.to_datetime(df[col_t]).dt.floor('60min')
        
        return df

    def prepare_dataframes(self):
        """Prepare dataframes for merging and remove unnecessary rows and columns.
        Args:
            Input dataframes.
        Return:
            Prepared input dataframes.
        """
        logger.info('Data Preprocessing...')
        (attendance, entity_schedule, link_attraction,
        parade_night_show, waiting_times,
        weather_data) = self.load_data()
        park_name = self.conf["load_preprocess"]["park_name"]
        attendance = attendance[attendance['FACILITY_NAME'] == park_name]
        lst_attr = link_attraction[link_attraction['PARK'] == park_name]['ATTRACTION']
        entity_schedule_pa = entity_schedule[entity_schedule['ENTITY_DESCRIPTION_SHORT'].isin(lst_attr)]
        waiting_times = waiting_times[waiting_times['ENTITY_DESCRIPTION_SHORT'].isin(lst_attr)]
        
        # Sort Dates and reset index
        attendance = self.sort_reset_date(attendance, 'USAGE_DATE')
        entity_schedule_pa = self.sort_reset_date(entity_schedule_pa, 'DEB_TIME')
        parade_night_show = self.sort_reset_date(parade_night_show, 'WORK_DATE')
        waiting_times = self.sort_reset_date(waiting_times, 'DEB_TIME')
        weather_data = self.sort_reset_date(weather_data, 'dt_iso')

        # Delete columns and some preprocessing
        weather_data['dt_iso'] = pd.to_datetime(weather_data['dt_iso'].str.replace(" +0000 UTC", "", regex=False), errors='coerce', format='%Y-%m-%d %H:%M:%S')
        weather_data = weather_data[["dt_iso", "weather_description"]]
        attendance.rename(columns={'USAGE_DATE': 'WORK_DATE'}, inplace=True)

        attendance['WORK_DATE'] = pd.to_datetime(attendance['WORK_DATE'])
        waiting_times['WORK_DATE'] = pd.to_datetime(waiting_times['WORK_DATE'])
        parade_night_show['WORK_DATE'] = pd.to_datetime(parade_night_show['WORK_DATE'])

        weather_data = self.hour_rounder(weather_data, col_t='dt_iso')
        waiting_times = self.hour_rounder(waiting_times, col_t='DEB_TIME')
        entity_schedule_pa = self.hour_rounder(entity_schedule_pa, col_t='DEB_TIME')
        logger.info('Data Preprocessed!')
        
        return waiting_times, attendance, entity_schedule_pa, parade_night_show, weather_data

    def merge_data(self):
        """Merging dataframes into one final dataframe for prediction

        Args:
            waiting_times: Dataframe containing waiting times
            attendance: Attendance dataframe containing attendance per day
            entity_schedule_pa: Dataframe containing maintenance data
            parade_night_show: Dataframe containing planned night shows and parades for the park
            weather_data: Weather dataframe

        Returns:
            df_m: Merged dataframe
        """
        
        logger.info('Merging Data...')
        (waiting_times, attendance,
        entity_schedule_pa, parade_night_show,
        weather_data) = self.prepare_dataframes()
        # Merge the dataframes
        df_m = waiting_times.merge(attendance[['WORK_DATE', 'attendance']], how='left', on='WORK_DATE')
        df_m = df_m.merge(entity_schedule_pa[['TIME_HOUR', 'ENTITY_DESCRIPTION_SHORT', 'REF_CLOSING_DESCRIPTION', 'ENTITY_TYPE', 'UPDATE_TIME']], how='left', on=['TIME_HOUR', 'ENTITY_DESCRIPTION_SHORT'])
        df_m = df_m.merge(parade_night_show, how='left', on='WORK_DATE')
        df_m = df_m.merge(weather_data, how='left', on='TIME_HOUR')
        logger.info('Data Merged!')    
        return df_m
    
    def remove_covid_period(self, df, col):
        """Removing covid period from dataset.

        Args:
            df: merged dataframe
            col: date column to filter on

        Returns:
            df: input dataframe without covid period
        """
        logger.info('Removing Covid data...')
        covid_date_min = self.conf["load_preprocess"]["covid_start_time"]
        df = df[df[col] <= covid_date_min]
        return df
    
    def get_full_input(self):
        """Removing covid period from dataset.

        Args:
            None

        Returns:
            df: merged input dataframes without covid data.
        """
        df = self.merge_data()
        df = self.remove_covid_period(df, "WORK_DATE")
        logger.info('Data ready for preprocessing!...')
        return df

    
