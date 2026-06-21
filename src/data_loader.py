import pandas as pd
import numpy as np

class DataLoader:
    def __init__(self, filepath='monthly_2000_2025_features.csv'):
        self.filepath = filepath
        self.df = None
        self.feature_cols = None
        self.lr_features = None
        self.event_dummies = []

    def load(self):
        df = pd.read_csv(self.filepath)
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
        df = df.sort_values('Date').reset_index(drop=True)

        for ec in sorted(df['Event_Label'].unique()):
            if ec != 0:
                df[f'Event_{int(ec)}'] = (df['Event_Label'] == ec).astype(int)

        self.event_dummies = [c for c in df.columns if c.startswith('Event_')]
        self.feature_cols = ['Year', 'Month', 'Month_Sin', 'Month_Cos',
                             'Price_Lag1', 'Price_Lag2', 'Price_Lag3'] + self.event_dummies
        self.lr_features = ['Year', 'Month_Sin', 'Month_Cos', 'Price_Lag1'] + self.event_dummies
        self.df = df
        return df

    def get_split_data(self, split_date='2021-01-01'):
        train_df = self.df[self.df['Date'] < split_date].copy()
        test_df = self.df[self.df['Date'] >= split_date].copy()

        X_train = train_df[self.feature_cols].values
        y_train = train_df['Price'].values
        X_test = test_df[self.feature_cols].values
        y_test = test_df['Price'].values

        lr_X_train = train_df[self.lr_features].values
        lr_X_test = test_df[self.lr_features].values

        return {
            'X_train': X_train, 'y_train': y_train,
            'X_test': X_test, 'y_test': y_test,
            'lr_X_train': lr_X_train, 'lr_X_test': lr_X_test,
            'test_dates': test_df['Date'].values,
            'train_df': train_df, 'test_df': test_df
        }

    def get_event_map(self):
        return {
            'Dot-com Crash': 'Dot-com Crash',
            '9/11 Attacks': '9/11 Attacks',
            'Global Financial Crisis': 'GFC',
            'European Debt Crisis': 'EU Debt Crisis',
            'Oil Price Crash': 'Oil Crash',
            'COVID-19 Pandemic': 'COVID-19',
            'Russia-Ukraine War': 'Rus-Ukr War'
        }

    def get_event_dates(self):
        return {
            'Dot-com Crash': '2000-03-01',
            '9/11 Attacks': '2001-09-01',
            'GFC': '2008-09-01',
            'EU Debt Crisis': '2010-04-01',
            'Oil Crash': '2014-06-01',
            'COVID-19': '2019-11-01',
            'Rus-Ukr War': '2022-02-01'
        }
