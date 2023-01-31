def format_number(number: int) -> str:
    """
    Formats a number as a string with the appropriate unit suffix.

    :param number: The number to format.
    :return: The formatted number string with the appropriate unit suffix.

    """
    if number >= 1000000000:
        formatted_number = '{:,.0f}B'.format(number / 1000000000)
    elif number >= 1000000:
        formatted_number = '{:,.0f}M'.format(number / 1000000)
    else:
        formatted_number = '{:,.0f}'.format(number)

    return formatted_number


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