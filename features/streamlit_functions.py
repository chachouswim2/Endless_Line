import pandas as pd
import numpy as np

def get_data_ready(df):
    """Perform preprocessing on a dataframe and return and cleaned dataframe.
    Args:
    df (pandas.DataFrame): Input DataFrame

    Returns:
    df (pandas.DataFrame): Cleaned DataFrame
    """
    df['WORK_DATE'] = pd.to_datetime(df['WORK_DATE'])
    df['year'] = df['WORK_DATE'].dt.year
    df['month'] = df['WORK_DATE'].dt.month
    df['day'] = df['WORK_DATE'].dt.day

    df['DEB_TIME'] = pd.to_datetime(df['DEB_TIME'])
    df['hour'] = df['DEB_TIME'].dt.hour
    df['minute'] = df['DEB_TIME'].dt.minute
    df['second'] = df['DEB_TIME'].dt.second 

    #Clean CAPACITY and ADJUST CAPACITY
    #Replace negative Guest carried
    df["GUEST_CARRIED"] = np.where(df["GUEST_CARRIED"] < 0, 0, df["GUEST_CARRIED"])

    #Drop rows with unconsistent behavior
    df = df[~((df['WORK_DATE'] == '2018-08-29') | 
          (df['WORK_DATE'] == '2019-01-03') | 
          (df['WORK_DATE'] == '2020-07-11') | 
          (df['WORK_DATE'] == '2021-08-30') & 
          (df['CAPACITY'] == 0) & 
          (df['ADJUST_CAPACITY'] == 0))]

    #If GUEST_CARRIED not null and CAPACITY = ADJUST_CAPACITY = 0, set their
    #values to GUEST_CARRIED
    df.loc[(df['WORK_DATE'] == '2019-10-01') & 
        (df['CAPACITY'] == 0) & 
        (df['ADJUST_CAPACITY'] == 0), 
        ['CAPACITY', 'ADJUST_CAPACITY']] = df['GUEST_CARRIED']

    #If GUEST_CARRIED not null and ADJUST_CAPACITY = 0, set its value to
    # CAPACITY
    df.loc[(df['GUEST_CARRIED'] != 0) & 
       (df['ADJUST_CAPACITY'] == 0) & 
       (df['CAPACITY'] != 0), 
       'ADJUST_CAPACITY'] = df['CAPACITY']

    # If GUEST_CARRIED not null and CAPACITY = 0, set CAPACITY 
    # to the biggest value between GUEST_CARRIED and ADJUST_CAPACITY
    df.loc[(df['GUEST_CARRIED'] != 0) & 
       (df['CAPACITY'] == 0), 
       'CAPACITY'] = df[['CAPACITY', 'GUEST_CARRIED']].max(axis=1)

    return df


def calculate_metrics(df, selected_year, selected_month, selected_day):
    if selected_year == "Select All" and selected_month == "Select All" and selected_day == "Select All":
        filtered_df = df
    elif selected_year != "Select All" and selected_month == "Select All" and selected_day == "Select All":
        filtered_df = df[(df['year'] == selected_year)]
    elif selected_year == "Select All" and selected_month != "Select All" and selected_day == "Select All":
        filtered_df = df[(df['month'] == selected_month)]
    elif selected_year == "Select All" and selected_month == "Select All" and selected_day != "Select All":
        filtered_df = df[(df['day'] == selected_day)]
    elif selected_year != "Select All" and selected_month != "Select All" and selected_day == "Select All":
        filtered_df = df[(df['year'] == selected_year) &
                        (df['month'] == selected_month)]
    elif selected_year != "Select All" and selected_month == "Select All" and selected_day != "Select All":
        filtered_df = df[(df['year'] == selected_year) &
                        (df['day'] == selected_day)]
    elif selected_year == "Select All" and selected_month != "Select All" and selected_day != "Select All":
        filtered_df = df[(df['day'] == selected_day) &
                        (df['month'] == selected_month)]
    elif selected_year != "Select All" and selected_month != "Select All" and selected_day != "Select All":
        filtered_df = df[(df['year'] == selected_year) &
                        (df['month'] == selected_month) &
                        (df['day'] == selected_day)]
    
    avg_wait_time = filtered_df['WAIT_TIME_MAX'].mean()
    capacity_utilization = (filtered_df['GUEST_CARRIED'].sum() / filtered_df['CAPACITY'].sum()) * 100
    avg_adjust_capacity_utilization = (filtered_df['GUEST_CARRIED'].sum() / filtered_df['ADJUST_CAPACITY'].sum()) * 100
    sum_attendance = filtered_df['attendance'].sum()

    return avg_wait_time, capacity_utilization, avg_adjust_capacity_utilization, sum_attendance


def calculate_delta(df, selected_year, selected_month, selected_day, avg_wait_time, capacity_utilization, avg_adjust_capacity_utilization, sum_attendance, delta, delta1, delta2, delta3):
    if selected_year == "Select All" and selected_month == "Select All" and selected_day == "Select All":
        delta = None
        delta1 = None
        delta2 = None
        delta3 = None

    if selected_year != "Select All" and selected_month == "Select All" and selected_day == "Select All":
        prev_year_df = df[(df['year'] == selected_year - 1)]
        if prev_year_df.empty:
            delta = None
            delta1 = None
            delta2 = None
            delta3 = None
        else:
            delta = round(avg_wait_time - prev_year_df['WAIT_TIME_MAX'].mean(),2)
            delta1 = round(capacity_utilization - ((prev_year_df['GUEST_CARRIED'].sum() / prev_year_df['CAPACITY'].sum()) * 100),2)
            delta2 = round(avg_adjust_capacity_utilization - ((prev_year_df['GUEST_CARRIED'].sum() / prev_year_df['ADJUST_CAPACITY'].sum()) * 100), 2)
            delta3 = round(sum_attendance - prev_year_df['attendance'].sum())

    elif selected_month != "Select All" and selected_year == "Select All" and selected_day == "Select All":
        prev_month_df = df[(df['month'] == selected_month-1)]
        if prev_month_df.empty:
            delta = None
            delta1 = None
            delta2 = None
            delta3 = None
        else:
            delta = round(avg_wait_time - prev_month_df['WAIT_TIME_MAX'].mean(), 2)
            delta1 = round(capacity_utilization - ((prev_month_df['GUEST_CARRIED'].sum() / prev_month_df['CAPACITY'].sum()) * 100),2)
            delta2 = round(avg_adjust_capacity_utilization - ((prev_month_df['GUEST_CARRIED'].sum() / prev_month_df['ADJUST_CAPACITY'].sum())* 100), 2)
            delta3 = round(sum_attendance - prev_month_df['attendance'].sum())


    elif selected_day != "Select All" and selected_year == "Select All" and selected_month == "Select All":
        prev_day_df = df[(df['day'] == selected_day - 1)]
        if prev_day_df.empty:
            delta = None
            delta1 = None
            delta2 = None
            delta3 = None
        else:
            delta = round(avg_wait_time - prev_day_df['WAIT_TIME_MAX'].mean(), 2)
            delta1 = round(capacity_utilization - ((prev_day_df['GUEST_CARRIED'].sum() / prev_day_df['CAPACITY'].sum()) * 100),2)
            delta2 = round(avg_adjust_capacity_utilization - ((prev_day_df['GUEST_CARRIED'].sum() / prev_day_df['ADJUST_CAPACITY'].sum()) * 100))
            delta3 = round(sum_attendance - prev_day_df['attendance'].sum())

    elif selected_year != "Select All" and selected_month != "Select All" and selected_day == "Select All":
        prev_month_year_df = df[(df['year'] == selected_year) &
                                       (df['month'] == selected_month-1)]
        if prev_month_year_df.empty:
            delta = None
            delta1 = None
            delta2 = None
            delta3 = None
        else:
            delta = round(avg_wait_time - prev_month_year_df['WAIT_TIME_MAX'].mean(), 2)
            delta1 = round(capacity_utilization - ((prev_month_year_df['GUEST_CARRIED'].sum() / prev_month_year_df['CAPACITY'].sum()) * 100),2)
            delta2 = round(avg_adjust_capacity_utilization - ((prev_month_year_df['GUEST_CARRIED'].sum() / prev_month_year_df['ADJUST_CAPACITY'].sum()) * 100))
            delta3 = round(sum_attendance - prev_month_year_df['attendance'].sum())

    elif selected_year != "Select All" and selected_month == "Select All" and selected_day != "Select All":
        prev_day_year_df = df[(df['year'] == selected_year) &
                                       (df['day'] == selected_day-1)]
        if prev_day_year_df.empty:
            delta = None
            delta1 = None
            delta2 = None
            delta3 = None
        else:
            delta = round(avg_wait_time - prev_day_year_df['WAIT_TIME_MAX'].mean(), 2)
            delta1 = round(capacity_utilization - ((prev_day_year_df['GUEST_CARRIED'].sum() / prev_day_year_df['CAPACITY'].sum()) * 100),2)
            delta2 = round(avg_adjust_capacity_utilization - ((prev_day_year_df['GUEST_CARRIED'].sum() / prev_day_year_df['ADJUST_CAPACITY'].sum()) * 100))
            delta3 = round(sum_attendance - prev_day_year_df['attendance'].sum())


    elif selected_year == "Select All" and selected_month != "Select All" and selected_day != "Select All":
        prev_day_month_df = df[(df['month'] == selected_month) &
                                       (df['day'] == selected_day-1)]
        if prev_day_month_df.empty:
            delta = None
            delta1 = None
            delta2 = None
            delta3 = None
        else:
            delta = round(avg_wait_time - prev_day_month_df['WAIT_TIME_MAX'].mean(), 2)
            delta1 = round(capacity_utilization - ((prev_day_month_df['GUEST_CARRIED'].sum() / prev_day_month_df['CAPACITY'].sum()) * 100),2)
            delta2 = round(avg_adjust_capacity_utilization - ((prev_day_month_df['GUEST_CARRIED'].sum() / prev_day_month_df['ADJUST_CAPACITY'].sum()) * 100))
            delta3 = round(sum_attendance - prev_day_month_df['attendance'].sum())

    elif selected_year != "Select All" and selected_month != "Select All" and selected_day != "Select All":
        prev_day_month_year_df = df[(df['year'] == selected_year) &
                                        (df['month'] == selected_month) &
                                       (df['day'] == selected_day-1)]
        if prev_day_month_year_df.empty:
            delta = None
            delta1 = None
            delta2 = None
            delta3 = None
        else:
            delta = round(avg_wait_time - prev_day_month_year_df['WAIT_TIME_MAX'].mean(), 2)
            delta1 = round(capacity_utilization - ((prev_day_month_year_df['GUEST_CARRIED'].sum() / prev_day_month_year_df['CAPACITY'].sum()) * 100),2)
            delta2 = round(avg_adjust_capacity_utilization - ((prev_day_month_year_df['GUEST_CARRIED'].sum() / prev_day_month_year_df['ADJUST_CAPACITY'].sum()) * 100))
            delta3 = round(sum_attendance - prev_day_month_year_df['attendance'].sum())
    else:
        delta = None
        delta1 = None
        delta2 = None
        delta3 = None

    return delta, delta1, delta2, delta3