import pandas as pd

def sort_reset_date(df, col_d='WORK_DATE'):
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

def hour_rounder(df, col_t='DEB_TIME'):
    """ Floor down the time to the hour to merge on weather data

    Args:
        df: dataframe to be modified
        col_t: column to be used for floor the time

    Returns:
        df: updated dataframe with new time floored to the hour
    """

    df['TIME_HOUR'] = pd.to_datetime(df[col_t]).dt.floor('60min')
    
    return df

def delta_time_parade(df):
    """ Calculate time difference between parades and night show (if existing) and the time at each time slot

    Args:
        df: dataframe to be updated

    Returns:
        df: updated dataframe with new columns
    """
    
    day_duration = (23 - 9) * 60
    
    df['delta_p1'] = 0
    df['delta_p2'] = 0
    df['delta_ns'] = 0
    df['normalized_delta_p1'] = 0
    df['normalized_delta_p2'] = 0
    df['normalized_delta_ns'] = 0

    deb_list_1 = pd.to_datetime(df[~df['PARADE_1'].isna()]['DEB_TIME']).dt.time
    deb_list_2 = pd.to_datetime(df[~df['PARADE_2'].isna()]['DEB_TIME']).dt.time
    deb_list_ns = pd.to_datetime(df[~df['NIGHT_SHOW'].isna()]['DEB_TIME']).dt.time

    parade_1_list = pd.to_datetime(df[~df['PARADE_1'].isna()]['PARADE_1'], format='%H:%M:%S').dt.time
    parade_2_list = pd.to_datetime(df[~df['PARADE_2'].isna()]['PARADE_2'], format='%H:%M:%S').dt.time
    parade_night_show = pd.to_datetime(df[~df['NIGHT_SHOW'].isna()]['NIGHT_SHOW'], format='%H:%M:%S').dt.time

    # df.loc[~df['PARADE_1'].isna(), 'delta_p1'] = [1-((abs(((c_d.hour - c_tt.hour)*60 + (c_d.minute - c_tt.minute))))/day_duration) for c_d, c_tt in zip(deb_list_1, parade_1_list)]

    df.loc[~df['PARADE_1'].isna(), 'delta_p1'] = [((c_d.hour - c_tt.hour)*60 + (c_d.minute - c_tt.minute)) for c_d, c_tt in zip(deb_list_1, parade_1_list)]
    df.loc[~df['PARADE_2'].isna(), 'delta_p2'] = [((c_d.hour - c_tt.hour)*60 + (c_d.minute - c_tt.minute)) for c_d, c_tt in zip(deb_list_2, parade_2_list)]
    df.loc[~df['NIGHT_SHOW'].isna(), 'delta_ns'] = [((c_d.hour - c_tt.hour)*60 + (c_d.minute - c_tt.minute)) for c_d, c_tt in zip(deb_list_ns, parade_night_show)]

    # df.loc[~df['PARADE_1'].isna(), 'normalized_delta_p1'] = [1-((abs(((c_d.hour - c_tt.hour)*60 + (c_d.minute - c_tt.minute))))/day_duration) for c_d, c_tt in zip(deb_list_1, parade_1_list)]
    # df.loc[~df['PARADE_2'].isna(), 'normalized_delta_p2'] = [1-((abs(((c_d.hour - c_tt.hour)*60 + (c_d.minute - c_tt.minute))))/day_duration) for c_d, c_tt in zip(deb_list_2, parade_2_list)]
    # df.loc[~df['NIGHT_SHOW'].isna(), 'normalized_delta_ns'] = [1-((abs(((c_d.hour - c_tt.hour)*60 + (c_d.minute - c_tt.minute))))/day_duration) for c_d, c_tt in zip(deb_list_ns, parade_night_show)]

    df.loc[~df['PARADE_1'].isna(), 'normalized_delta_p1'] = [1-(abs(c_d)/day_duration) for c_d in df[~df['PARADE_1'].isna()]['delta_p1']]
    df.loc[~df['PARADE_2'].isna(), 'normalized_delta_p2'] = [1-(abs(c_d)/day_duration) for c_d in df[~df['PARADE_2'].isna()]['delta_p2']]
    df.loc[~df['NIGHT_SHOW'].isna(), 'normalized_delta_ns'] = [1-(abs(c_d)/day_duration) for c_d in df[~df['NIGHT_SHOW'].isna()]['delta_ns']]

    return df

def load_data(data_path):
    """ Load all the attendance, weather and waiting data

    Returns:
        attendance, entity_schedule, link_attraction, parade_night_show, waiting_times, weather_data: All dataframes returned by the function
    """
    
    print('Data Loading...')
    attendance = pd.read_csv(data_path+r'/attendance.csv')
    entity_schedule = pd.read_csv(data_path+r'/entity_schedule.csv')
    # glossary = pd.read_excel(r'data/glossary.xlsx')
    link_attraction = pd.read_csv(data_path+r'/link_attraction_park.csv', sep=';')
    parade_night_show = pd.read_excel(data_path+r'/parade_night_show.xlsx')
    waiting_times = pd.read_csv(data_path+r'/waiting_times.csv')
    weather_data = pd.read_csv(data_path+r'/weather_data.csv')

    parade_night_show.drop(columns=['Unnamed: 0'], inplace=True)
    print('Data Loaded!')

    return attendance, entity_schedule, link_attraction, parade_night_show, waiting_times, weather_data

def preprocessing_data(attendance, entity_schedule, link_attraction, parade_night_show, waiting_times, weather_data):
    """ Basic preprocessing and data clearning to allow merging

    Args:
        attendance: Attendance dataframe containing attendance per day
        entity_schedule: Dataframe containing maintenance data
        link_attraction: Dataframe linking attractions to respective parks
        parade_night_show: Dataframe containing planned night shows and parades for the park
        waiting_times: Dataframe containing waiting times
        weather_data: Weather dataframe

    Returns:
        waiting_times, attendance, entity_schedule_pa, parade_night_show, weather_data: Preprocessed and cleaned dataframes ready for merging
    """
    print('Data Preprocessing...')
    attendance = attendance[attendance['FACILITY_NAME'] == 'PortAventura World']
    lst_attr = link_attraction[link_attraction['PARK'] == 'PortAventura World']['ATTRACTION']
    entity_schedule_pa = entity_schedule[entity_schedule['ENTITY_DESCRIPTION_SHORT'].isin(lst_attr)]
    waiting_times = waiting_times[waiting_times['ENTITY_DESCRIPTION_SHORT'].isin(lst_attr)]
    attendance = attendance[attendance['attendance']>=0]
    
    # Sort Dates and reset index
    attendance = sort_reset_date(attendance, 'USAGE_DATE')
    entity_schedule_pa = sort_reset_date(entity_schedule_pa, 'DEB_TIME')
    parade_night_show = sort_reset_date(parade_night_show, 'WORK_DATE')
    waiting_times = sort_reset_date(waiting_times, 'DEB_TIME')
    weather_data = sort_reset_date(weather_data, 'dt_iso')

    # Delete columns and some preprocessing
    weather_data['dt_iso'] = pd.to_datetime(weather_data['dt_iso'].str.replace(" +0000 UTC", "", regex=False), errors='coerce', format='%Y-%m-%d %H:%M:%S')
    cols_del = ['city_name', 'lat', 'lon', 'weather_id', 'visibility', 'sea_level', 'grnd_level', 'wind_gust', 'snow_3h']
    weather_data.drop(columns=cols_del, inplace=True)
    weather_data.fillna(0, inplace=True)
    attendance.rename(columns={'USAGE_DATE': 'WORK_DATE'}, inplace=True)
    # weather_data.rename(columns={'dt_iso': 'TIME_HOUR'}, inplace=True)

    attendance['WORK_DATE'] = pd.to_datetime(attendance['WORK_DATE'])
    waiting_times['WORK_DATE'] = pd.to_datetime(waiting_times['WORK_DATE'])
    parade_night_show['WORK_DATE'] = pd.to_datetime(parade_night_show['WORK_DATE'])

    weather_data = hour_rounder(weather_data, col_t='dt_iso')
    waiting_times = hour_rounder(waiting_times, col_t='DEB_TIME')
    entity_schedule_pa = hour_rounder(entity_schedule_pa, col_t='DEB_TIME')
    print('Data Preprocessed!')
    
    return waiting_times, attendance, entity_schedule_pa, parade_night_show, weather_data

def merge_data(waiting_times, attendance, entity_schedule_pa, parade_night_show, weather_data):
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
    
    print('Merging Data...')
    # Merge the dataframes
    df_m = waiting_times.merge(attendance[['WORK_DATE', 'attendance']], how='left', on='WORK_DATE')
    df_m = df_m.merge(entity_schedule_pa[['TIME_HOUR', 'ENTITY_DESCRIPTION_SHORT', 'REF_CLOSING_DESCRIPTION', 'ENTITY_TYPE', 'UPDATE_TIME']], how='left', on=['TIME_HOUR', 'ENTITY_DESCRIPTION_SHORT'])
    df_m = df_m.merge(parade_night_show, how='left', on='WORK_DATE')
    df_m = df_m.merge(weather_data, how='left', on='TIME_HOUR')
    print('Data Merged!')
    
    return df_m

def create_df(data_path):
    """ Function combining all loading, preprocessing and merging functions

    Returns:
        df_m: Merged and finalized dataframe
    """
    
    attendance, entity_schedule, link_attraction, parade_night_show, waiting_times, weather_data = load_data(data_path)
    waiting_times, attendance, entity_schedule_pa, parade_night_show, weather_data = preprocessing_data(attendance, entity_schedule, link_attraction, parade_night_show, waiting_times, weather_data)
    df_m = merge_data(waiting_times, attendance, entity_schedule_pa, parade_night_show, weather_data)
    df_m = delta_time_parade(df_m)
    
    # cols_del = ['dt', 'dt_iso', 'timezone', 'NIGHT_SHOW', 'PARADE_1', 'PARADE_2', 'TIME_HOUR', 'DEB_TIME_HOUR']
    # df_m.drop(columns=cols_del, inplace=True)
    
    print('Dataframe Finalized!')

    return df_m