import pandas as pd
import numpy as np

class EventAnalyzer:
    @staticmethod
    def get_event_stats(df):
        event_windows = {
            'Dot-com': ('2000-03-01', '2002-10-01'),
            '9/11': ('2001-09-01', '2002-03-01'),
            'GFC': ('2008-09-01', '2009-12-01'),
            'EU Debt': ('2010-04-01', '2012-12-01'),
            'Oil Crash': ('2014-06-01', '2015-12-01'),
            'COVID-19': ('2019-11-01', '2021-12-01'),
            'War': ('2022-02-01', '2025-07-01'),
        }
        def classify_event(date):
            for event, (s, e) in event_windows.items():
                if pd.to_datetime(s) <= date <= pd.to_datetime(e):
                    return event
            return 'Normal'
        df['Period'] = df['Date'].apply(classify_event)
        df['Monthly_Return'] = df['Price'].pct_change() * 100
        stats = df.groupby('Period').agg(
            mean=('Price', 'mean'),
            std=('Price', 'std'),
            min=('Price', 'min'),
            max=('Price', 'max'),
            count=('Price', 'count'),
            volatility=('Monthly_Return', lambda x: x.std())
        ).round(2)
        return stats.sort_values('volatility', ascending=False)

    @staticmethod
    def get_top_features(feature_importances, feature_cols, top_n=10):
        feat_df = pd.DataFrame({'feature': feature_cols, 'importance': feature_importances})
        return feat_df.sort_values('importance', ascending=False).head(top_n)

    @staticmethod
    def compute_forecast(current_features, model_trainer, model_name, feature_cols, lr_features, steps=6):
        forecasts = []
        cf = current_features.copy()
        for i in range(steps):
            pred = model_trainer.predict(model_name, cf, feature_cols, lr_features)
            forecasts.append(pred)
            new_month = (cf['Month'] % 12) + 1
            cf.update({
                'Month': new_month,
                'Month_Sin': np.sin(2 * np.pi * new_month / 12),
                'Month_Cos': np.cos(2 * np.pi * new_month / 12),
                'Price_Lag3': cf.get('Price_Lag2', cf['Price_Lag1']),
                'Price_Lag2': cf.get('Price_Lag1', cf['Price_Lag1']),
                'Price_Lag1': pred,
            })
        return forecasts
