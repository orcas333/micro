import numpy as np
import pandas as pd
import pendulum
import datetime as dt

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# SDGE account: 40126764291
# https://www.sdge.com/node/15291


def ETL_data(df):

    # ETL-ing some data. All these hacky lambda functions are quite ugly - fix. 
    df['timestamp_end_raw'] = df['interval_end'].apply(lambda x: dt.datetime.strptime(x, '%m/%d/%Y %H:%M'))
    df['timestamp_start_raw'] = df['interval_start'].apply(lambda x: dt.datetime.strptime(x, '%m/%d/%Y %H:%M'))

    df['hour_end'] = df['timestamp_end_raw'].apply(lambda x: x.hour)
    df['hour_start'] = df['timestamp_start_raw'].apply(lambda x: x.hour)
    df['day'] = df['timestamp_end_raw'].apply(lambda x: x.day)
    df['month'] = df['timestamp_end_raw'].apply(lambda x: x.month)
    df['year'] = df['timestamp_end_raw'].apply(lambda x: x.year)
    df['day_of_week'] = df['timestamp_end_raw'].apply(lambda x: x.weekday())
    df['weekend'] = df['day_of_week'].apply(lambda x: 1 if (x == 0 or x == 1) else 0)

    df['time_str'] = df['interval_end'].apply(lambda x: pendulum.parse(
        x, strict=False).to_time_string())
    df['time'] = df['time_str'].apply(lambda x: dt.datetime.strptime(
        x, '%H:%M:%S'))

    # Hard-coding in a simplified TOU period very quickly
    df['tou_period'] =  df['hour_start'].apply(lambda x: 'on_peak' if x in range(14,22) else ('super_off_peak' if x in range(0,7) else 'off_peak'))

    return df


def plot_data(df):

    fig = px.line(df, x=df.time, y=df.interval_kW, color=df.month)
    fig.show()


def plot_monthly_data(df):
    unique_months = df['month'].unique()[::-1]

    fig = make_subplots(
        rows=1, cols=len(unique_months))

    for key, month in enumerate(unique_months):
        month_df = df[df['month'] == month]
        fig.add_trace(go.Scatter(x=month_df.time,
                                 y=month_df.interval_kW), row=1, col=key+1)

        # Update x and y axis properties
        fig.update_xaxes(
            title_text=f"timestamp in month {month}", row=1, col=key+1)
        fig.update_yaxes(title_text="kW", range=[0, 8], row=1, col=key+1)

    fig.update_layout(height=750, width=2000,
                      title_text="Daily kW Usage by Month")

    fig.show()


def plot_monthly_interval_data(df):
    unique_months = df['month'].unique()[::-1]

    fig = make_subplots(
        rows=len(unique_months), cols=1)

    for key, month in enumerate(unique_months):
        month_df = df[df['month'] == month]
        
        fig.add_trace(go.Scatter(x=month_df.timestamp_raw,
                                 y=month_df.interval_kW,
                                 mode='lines+markers',
                                 marker_color=month_df['weekend']),
                                 row=key+1, col=1)

        # Update x and y axis properties
        fig.update_xaxes(
            title_text=f"timestamp in month {month}", row=key+1, col=1)
        fig.update_yaxes(title_text="kW", range=[0, 8], row=key+1, col=1)

    fig.update_layout(height=2000, width=4000,
                      title_text="Daily kW Usage by Month")

    fig.show()

if __name__ == "__main__":

    df=pd.read_csv('intervals_40126764291.csv')
    data=ETL_data(df)
    # data.to_csv('HUJH1001_ETL.csv')
    plot_data(data)
    plot_monthly_data(data)
    plot_monthly_interval_data(data)
