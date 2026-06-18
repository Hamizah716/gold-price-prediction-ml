import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from src.data_loader import DataLoader
from src.models import ModelTrainer
from src.visualization import Visualizer
from src.analysis import EventAnalyzer

st.set_page_config(page_title="Gold Price Predictor", layout="wide")
st.title("Analyzing the Impact of Global Events on Gold Prices Using ML Models")
st.caption("Hamizah Aziim Bhikan | M.Sc. Data Science | Research Project Semester IV")
st.markdown("---")

@st.cache_data
def load_data():
    loader = DataLoader()
    df = loader.load()
    return df, loader

@st.cache_resource
def train():
    loader = DataLoader()
    loader.load()
    data_dict = loader.get_split_data()
    trainer = ModelTrainer()
    results = trainer.train(data_dict)
    return trainer, results, data_dict, loader

df, loader = load_data()
trainer, results, data_dict, _ = train()
y_test = data_dict['y_test']
test_dates = data_dict['test_dates']
analyzer = EventAnalyzer()

models_to_show = ['Linear Regression', 'Random Forest', 'XGBoost', 'Neural Network']

tab1, tab2, tab3, tab4 = st.tabs(["Data Overview", "Model Performance", "Prediction", "Event Analysis"])

with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Gold Price Data (2000-2025)")
        st.dataframe(df[['Date', 'Price', 'Major_Event']].tail(10), use_container_width=True)
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Total Records", len(df))
        col_b.metric("Date Range", f"{df['Date'].min().date()} to {df['Date'].max().date()}")
        col_c.metric("Max Price", f"${df['Price'].max():.2f}")

        with st.expander("Show Full Cleaned Dataset"):
            st.dataframe(df, use_container_width=True)
            st.download_button(
                "Download Cleaned Data (CSV)",
                df.to_csv(index=False).encode(),
                file_name="gold_price_cleaned.csv",
                mime="text/csv",
            )
    with col2:
        st.subheader("Gold Price Trend")
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df['Date'], df['Price'], color='#DAA520', linewidth=1.5)
        ax.fill_between(df['Date'], df['Price'], alpha=0.15, color='#DAA520')
        ax.set_ylabel('Price (USD/oz)')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

with tab2:
    st.subheader("Model Performance Comparison")
    col1, col2 = st.columns([1, 1.5])

    perf_data = [[n, f'{r["RMSE"]:.2f}', f'{r["MAE"]:.2f}', f'{r["MAPE"]:.2f}%']
                 for n, r in results.items()]
    perf_df = pd.DataFrame(perf_data, columns=['Model', 'RMSE', 'MAE', 'MAPE (%)'])

    with col1:
        st.table(perf_df)
        st.markdown("""
        **Key Insights:**
        - **Neural Network** achieves lowest error (MAPE: {:.2f}%)
        - Tree models struggle with extrapolation
        - Event-aware features improve predictions
        """.format(results['Neural Network']['MAPE']))

    with col2:
        selected = st.selectbox("Select Model", models_to_show)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(pd.to_datetime(test_dates), y_test, 'b-', label='Actual', linewidth=2, alpha=0.8)
        ax.plot(pd.to_datetime(test_dates), results[selected]['predictions'],
                'r--', label=f'{selected}', linewidth=2, alpha=0.8)
        ax.set_title(f'{selected} - Actual vs Predicted', fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Gold Price (USD/oz)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        st.pyplot(fig)

with tab3:
    st.subheader("Gold Price Prediction")
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Enter Input Features")
        year = st.number_input("Year", min_value=2025, max_value=2030, value=2025)
        month = st.slider("Month", 1, 12, 6)
        lag1 = st.number_input("Price Lag 1 (prev month)", value=df['Price'].iloc[-1])
        lag2 = st.number_input("Price Lag 2", value=df['Price'].iloc[-2])
        lag3 = st.number_input("Price Lag 3", value=df['Price'].iloc[-3])
        event_label = st.selectbox("Event Type", [4, 0, 1, 2, 3, 5, 6],
                                   format_func=lambda x: {1: 'COVID-19', 3: 'GFC', 2: 'EU Debt',
                                                          4: 'Normal', 5: 'Oil Crash', 0: '9/11', 6: 'War'}.get(x, 'Normal'))

    with col2:
        st.markdown("### Predict Gold Price")
        model_choice = st.radio("Choose Model", models_to_show)

        input_dict = {
            'Year': year, 'Month': month,
            'Month_Sin': np.sin(2 * np.pi * month / 12),
            'Month_Cos': np.cos(2 * np.pi * month / 12),
            'Price_Lag1': lag1, 'Price_Lag2': lag2, 'Price_Lag3': lag3,
        }
        for ec in sorted(df['Event_Label'].unique()):
            if ec != 4:
                input_dict[f'Event_{int(ec)}'] = 1 if event_label == ec else 0

        pred_price = trainer.predict(model_choice, input_dict, loader.feature_cols, loader.lr_features)

        st.markdown(f"### Predicted Gold Price: **${pred_price:.2f}**")
        st.markdown(f"Using **{model_choice}** model")

        if st.button("Forecast Next 6 Months"):
            with st.spinner("Generating forecast..."):
                forecasts = analyzer.compute_forecast(
                    input_dict, trainer, model_choice,
                    loader.feature_cols, loader.lr_features
                )
                fig, ax = plt.subplots(figsize=(10, 4))
                ax.plot(range(1, 7), forecasts, 'go-', linewidth=2, markersize=8)
                ax.set_xlabel('Month Ahead'); ax.set_ylabel('Predicted Price (USD/oz)')
                ax.set_title(f'6-Month Forecast ({model_choice})')
                ax.grid(True, alpha=0.3)
                for i, v in enumerate(forecasts):
                    ax.text(i + 1, v + 10, f'${v:.0f}', ha='center', fontsize=9)
                st.pyplot(fig)

with tab4:
    st.subheader("Impact of Global Events on Gold Prices")
    col1, col2 = st.columns([1, 1])

    with col1:
        stats = analyzer.get_event_stats(df)
        st.dataframe(stats, use_container_width=True)

        st.markdown("### Gold Price Trend with Events")
        event_colors_viz = {
            '9/11 Attacks': 'red', 'GFC': 'darkred', 'EU Debt Crisis': 'purple',
            'COVID-19': 'orange', 'Oil Crash': 'brown', 'Rus-Ukr War': 'magenta'
        }
        viz = Visualizer()
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(df['Date'], df['Price'], 'b-', linewidth=1.5, label='Gold Price')
        for label, dt_str in loader.get_event_dates().items():
            dt = pd.to_datetime(dt_str)
            clr = event_colors_viz.get(label, 'red')
            ax.axvline(x=dt, color=clr, linestyle='--', alpha=0.6, linewidth=1.2)
        ax.set_title('Gold Price with Major Global Events')
        ax.set_xlabel('Date'); ax.set_ylabel('Price (USD/oz)')
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    with col2:
        st.markdown("### Data Explorer")
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        col = st.selectbox("Select Column", num_cols)
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        ax2.plot(df['Date'], df[col], linewidth=1.5, color='darkblue')
        ax2.set_title(f'{col} Over Time'); ax2.set_xlabel('Date'); ax2.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        st.pyplot(fig2)

        st.markdown("### Event Volatility")
        event_windows = {
            '9/11': ('2001-06-01', '2002-06-01'),
            'GFC': ('2008-06-01', '2009-12-01'),
            'EU Debt': ('2010-01-01', '2012-12-01'),
            'COVID-19': ('2020-01-01', '2020-12-01'),
            'Oil Crash': ('2014-06-01', '2015-12-01'),
            'War': ('2022-01-01', '2023-01-01'),
        }
        def classify_event(date):
            for event, (s, e) in event_windows.items():
                if pd.to_datetime(s) <= date <= pd.to_datetime(e):
                    return event
            return 'Normal'
        df['Period'] = df['Date'].apply(classify_event)
        vols = df.groupby('Period')['Price'].std().sort_values(ascending=False)
        fig3, ax3 = plt.subplots(figsize=(10, 4))
        clrs = ['#2B579A', '#E81123', '#FF8C00', '#7B2D8E', '#107C10', '#00B7C3', '#FFB900']
        ax3.bar(vols.index, vols.values, color=clrs[:len(vols)])
        ax3.set_ylabel('Std Dev (USD/oz)')
        ax3.set_title('Gold Price Volatility by Event Period')
        plt.xticks(rotation=45)
        st.pyplot(fig3)
