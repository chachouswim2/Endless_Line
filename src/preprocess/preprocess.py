"""Preprocess input data and add features."""
import pandas as pd
import numpy as np
import warnings
import logging
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import FunctionTransformer

warnings.filterwarnings("ignore")
logger = logging.getLogger("main_logger")

warnings.filterwarnings("ignore")

class Preprocess():
    """Preprocess data and add features.."""
    def __init__(self, conf, data):
        self.conf = conf
        self.data = data
    
    def clean_data(self, df):
        """Clean dataframe of NaNs and inconsistencies in data.
        Args:
            data: input dataframe.
        Returns:
            df: cleaned input dataframe.
        """
        mean = df.loc[(df.WORK_DATE >= pd.to_datetime("2019-01-01")) & (df.WORK_DATE < pd.to_datetime("2019-06-01")), "attendance"].mean()
        df["attendance"].fillna(mean, inplace=True)
        df.loc[df.GUEST_CARRIED<0, "GUEST_CARRIED"] = 0
        df.loc[(df.CAPACITY>0) & (df.ADJUST_CAPACITY==0) & (df.GUEST_CARRIED==0), "CAPACITY"] = 0
        df.loc[(df.CAPACITY==0) & (df.ADJUST_CAPACITY>0) & (df.GUEST_CARRIED==0), "ADJUST_CAPACITY"] = 0
        df.loc[(df.CAPACITY==0) & (df.ADJUST_CAPACITY>0) & (df.GUEST_CARRIED>0), "CAPACITY"] = df.loc[(df.CAPACITY==0) & (df.ADJUST_CAPACITY>0) & (df.GUEST_CARRIED>0), "ADJUST_CAPACITY"]
        df.loc[(df.CAPACITY>0) & (df.ADJUST_CAPACITY==0) & (df.GUEST_CARRIED>0), "ADJUST_CAPACITY"] = df.loc[(df.CAPACITY>0) & (df.ADJUST_CAPACITY==0) & (df.GUEST_CARRIED>0), "CAPACITY"]
        df = df[(df.CAPACITY != 0) & (df.ADJUST_CAPACITY!=0) & (df.GUEST_CARRIED>0)]
        df.loc[df.UP_TIME == -1, "UP_TIME"] = 15

        return df

    def delta_time_parade(self, df):
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

        df.loc[~df['PARADE_1'].isna(), 'delta_p1'] = [((c_d.hour - c_tt.hour)*60 + (c_d.minute - c_tt.minute)) for c_d, c_tt in zip(deb_list_1, parade_1_list)]
        df.loc[~df['PARADE_2'].isna(), 'delta_p2'] = [((c_d.hour - c_tt.hour)*60 + (c_d.minute - c_tt.minute)) for c_d, c_tt in zip(deb_list_2, parade_2_list)]
        df.loc[~df['NIGHT_SHOW'].isna(), 'delta_ns'] = [((c_d.hour - c_tt.hour)*60 + (c_d.minute - c_tt.minute)) for c_d, c_tt in zip(deb_list_ns, parade_night_show)]

        df.loc[~df['PARADE_1'].isna(), 'normalized_delta_p1'] = [1-(abs(c_d)/day_duration) for c_d in df[~df['PARADE_1'].isna()]['delta_p1']]
        df.loc[~df['PARADE_2'].isna(), 'normalized_delta_p2'] = [1-(abs(c_d)/day_duration) for c_d in df[~df['PARADE_2'].isna()]['delta_p2']]
        df.loc[~df['NIGHT_SHOW'].isna(), 'normalized_delta_ns'] = [1-(abs(c_d)/day_duration) for c_d in df[~df['NIGHT_SHOW'].isna()]['delta_ns']]

        return df
    
    def delta_openings(self, df):
        """ Calculate time difference between opening and closing of park and the time at each time slot

        Args:
            df: dataframe to be updated

        Returns:
            df: updated dataframe with new columns
        """
        df["timet"] = [((c_d.hour - 9)*4 + c_d.minute/15) for c_d in pd.to_datetime(df["DEB_TIME"]).dt.time]
        df["delta_open_scaled"] = df["attendance"]
        df.loc[df["timet"]<12, "delta_open_scaled"] = (df[df["timet"]<12]["attendance"]*df[df["timet"]<12]["timet"]/12)
        df.loc[df["timet"]>27, "delta_open_scaled"] = (((55-df[df["timet"]>27]["timet"])/28)*df[df["timet"]>27]["attendance"])
        df["delta_open_normalized"] = 1
        df.loc[df["timet"]<12, "delta_open_normalized"] = (df[df["timet"]<12]["timet"]/12)
        df.loc[df["timet"]>27, "delta_open_normalized"] = ((55-df[df["timet"]>27]["timet"])/28)   
        return df
    
    def sin_transformer(self, period):
        """Create sinusoidal transformer.
        Args:
            period: period for transformation.
        Returns:
            Array of transformed data.
        """
        return FunctionTransformer(lambda x: np.sin(x / period * 2 * np.pi))

    def cos_transformer(self, period):
        """Create cosine transformer.
        Args:
            period: period for transformation.
        Returns:
            Array of transformed data.
        """
        return FunctionTransformer(lambda x: np.cos(x / period * 2 * np.pi))
    
    def temporal_features(self, df):
        """Add teamporal features to dataframe.
        Args:
            df: dataframe to be updated
        Returns:
            df: updated dataframe with new columns
        """
        df["year"] = df.WORK_DATE.dt.year
        df["month"] = df.WORK_DATE.dt.month
        df["day"] = df.WORK_DATE.dt.day
        df["weekday"] = df.WORK_DATE.dt.weekday
        df["weekend"] = df["weekday"].apply(lambda x: 1 if x>4 else 0)
        df.DEB_TIME = pd.to_datetime(df.DEB_TIME)
        df.FIN_TIME = pd.to_datetime(df.FIN_TIME)
        df["hour"] = df.DEB_TIME.dt.hour
        df["minute"] = df.DEB_TIME.dt.minute
        df["month_sin"] = self.sin_transformer(12).fit_transform(df["month"])
        df["month_cos"] = self.cos_transformer(12).fit_transform(df["month"])
        df["day_sin"] = self.sin_transformer(31).fit_transform(df["day"])
        df["day_cos"] = self.cos_transformer(31).fit_transform(df["day"])
        df["minute_sin"] = self.sin_transformer(60).fit_transform(df["minute"])
        df["minute_cos"] = self.cos_transformer(60).fit_transform(df["minute"])
        df["weekday_sin"] = self.sin_transformer(7).fit_transform(df["weekday"])
        df["weekday_cos"] = self.cos_transformer(7).fit_transform(df["weekday"])
        df["hour_sin"] = self.sin_transformer(24).fit_transform(df["hour"])
        df["hour_cos"] = self.cos_transformer(24).fit_transform(df["hour"])
        
        return df
    
    def weather_ordinal_encoding(self, df):
        """Transform the weather description to an ordinal encoding, taking into account the intensity of the weather.
        Args:
            df: dataframe to be updated
        Returns:
            df: updated dataframe with new columns
        """
        list_weather = (df[["WAIT_TIME_MAX", "weather_description"]].groupby(by=["weather_description"]).mean()).sort_values(by="WAIT_TIME_MAX").index.tolist()
        ordinal_encoder = OrdinalEncoder(categories=[list_weather])
        df["weather_description"] = ordinal_encoder.fit_transform(df.weather_description.values.reshape(-1,1))
        return df
    
    def remove_cols(self, df):
        """Remove unnecessary columns from dataframe for training.
        Args:
            df: dataframe to be updated
        Returns:
            df: updated dataframe with new columns
        """
        col_to_drop = self.conf["load_preprocess"]["col_to_drop"]
        df.drop(columns=col_to_drop, inplace=True)
        return df
    
    def create_final_input(self):
        """ Function combining all preprocessing functions.

        Returns:
            df: Merged and finalized dataframe
        """
        logger.info('Preprocessing dataframe')
        df = self.data
        df = self.clean_data(df)
        df = self.delta_time_parade(df)
        df = self.delta_openings(df)
        df = self.temporal_features(df)
        df = self.weather_ordinal_encoding(df)
        df = self.remove_cols(df)
        
        logger.info('Dataframe Finalized!')

        return df