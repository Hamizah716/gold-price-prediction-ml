import pandas as pd
import numpy as np

class EventAnalyzer:
    @staticmethod
    def get_event_stats(df):
        event_map = {
            'COVID-19 Pandemic': 'COVID-19', '9/11 Terror Attacks': '9/11',
            'Lehman Brothers Collapse': 'GFC', 'European Debt Crisis': 'EU Debt',
            'Oil Price Crash': 'Oil Crash', 'Russia-Ukraine War': 'War', 'None': 'Normal'
        }
        df['Event_Short'] = df['Major_Event'].map(event_map).fillna('Normal')
        stats = df.groupby('Event_Short')['Price'].agg(['mean', 'std', 'min', 'max', 'count'])
        return stats.round(2)

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
