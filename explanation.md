# Gold Price Prediction ML — External Exam Preparation

## Project Title
**Analyzing the Impact of Global Events on Gold Prices Using Machine Learning Models**

## Live App
https://gold-price-prediction-ml-f7cgv3jknks3vzdqs3esyz.streamlit.app/

## GitHub Repo
https://github.com/RammoKun/gold-price-prediction-ml

---

## 1. What Does This Project Do?

A **Streamlit web application** that:
- Analyzes 25 years of gold price data (2000–2025)
- Trains 4 machine learning models to predict gold prices
- Shows how major global events (wars, pandemics, financial crises) affect gold prices
- Lets users input custom values and get real-time price predictions + 6-month forecasts
- Deployed online — no installation needed, works in any browser

---

## 2. Dataset

| Detail | Value |
|---|---|
| **Source** | DataHub Core Gold Prices |
| **Frequency** | Monthly |
| **Period** | January 2000 – July 2025 |
| **Total Records** | 307 |
| **Target Variable** | Gold Price (USD per troy ounce) |

### Events Analyzed

| Event | Year | Type |
|---|---|---|
| 9/11 Terror Attacks | 2001 | Geopolitical |
| Global Financial Crisis | 2008 | Economic |
| European Debt Crisis | 2010 | Economic |
| Oil Price Crash | 2014 | Economic |
| COVID-19 Pandemic | 2020 | Health Crisis |
| Russia-Ukraine War | 2022 | Geopolitical |

### Features Engineered

- **Lag variables:** Price_Lag1, Price_Lag2, Price_Lag3 (previous months' prices)
- **Moving averages:** MA3, MA6 (3-month and 6-month rolling averages)
- **Cyclical encoding:** Month_Sin, Month_Cos (captures seasonality)
- **Event dummies:** Binary indicators for each event type
- **Year:** Captures long-term upward trend

---

## 3. Machine Learning Models

### 3.1 Linear Regression
- **What:** Statistical baseline — finds best straight-line relationship between features and price
- **Why used:** Simple, interpretable, establishes a baseline
- **Performance (MAPE):** 2.58%
- **Limitation:** Assumes linear relationships — fails during volatile/shock periods

### 3.2 Random Forest
- **What:** Ensemble of 200 decision trees, averages their predictions
- **Why used:** Captures non-linear patterns, gives feature importance scores
- **Performance (MAPE):** 11.67%
- **Limitation:** Cannot predict values outside training range (no extrapolation)

### 3.3 XGBoost
- **What:** Gradient boosting with 200 estimators, learning rate 0.05
- **Why used:** State-of-the-art for tabular data, handles complex interactions
- **Performance (MAPE):** 12.46%
- **Limitation:** Same extrapolation issue as Random Forest

### 3.4 Neural Network (MLP Regressor)
- **What:** 3 hidden layers (128 → 64 → 32 neurons), ReLU activation, Adam optimizer
- **Why used:** Can learn complex non-linear relationships AND extrapolate
- **Performance (MAPE):** 6.10%
- **Advantage:** Best balance of accuracy and robustness

### Model Performance Summary

| Model | RMSE | MAE | MAPE |
|---|---|---|---|
| Linear Regression | 73.99 | 55.98 | 2.58% |
| Random Forest | 519.79 | 307.98 | 11.67% |
| XGBoost | 541.14 | 326.51 | 12.46% |
| Neural Network | 212.56 | 148.52 | 6.10% |

---

## 4. Training Methodology

### Chronological Train/Test Split
- **Train:** January 2000 – December 2020 (252 observations)
- **Test:** January 2021 – July 2025 (55 observations)
- **Why chronological?** In time-series, using random split would leak future data into training, giving unrealistic performance. Chronological split evaluates models on truly unseen future data.

### Feature Scaling
- MinMaxScaler normalizes all features to [0, 1] range
- Prevents features with larger values from dominating the model

### Why Not LSTM / Deep Learning?
- Python 3.14 does not yet support TensorFlow/PyTorch
- LSTM can be run on Google Colab and integrated later (mentioned in Future Work)

---

## 5. App Architecture (4 Tabs)

### Tab 1: Data Overview
- Shows gold price dataset table
- Key metrics: Total Records, Date Range, Max Price
- Gold price trend chart (2000–2025)
- **"Show Full Cleaned Dataset"** expander with CSV download button

### Tab 2: Model Performance
- Performance metrics table (RMSE, MAE, MAPE for all 4 models)
- Dropdown to select any model and view its actual vs predicted graph
- Key Insight text explaining which model performs best

### Tab 3: Prediction
- **Input fields:** Year, Month, Price_Lag1, Price_Lag2, Price_Lag3, Event Type
- **Model selector:** Choose which ML model to use
- **Output:** Predicted gold price displayed prominently
- **6-Month Forecast:** Button that generates predictions for next 6 months by feeding each prediction back as input (iterative forecasting), shown as a line chart with values

### Tab 4: Event Analysis
- Event statistics table (mean price, volatility, count per event type)
- Gold price timeline with vertical markers at major event dates
- Data explorer — select any numeric column to view its trend
- Volatility comparison bar chart — shows which events caused most price fluctuation

---

## 6. Key Findings

1. **Gold is a safe-haven asset:**
   - During Russia-Ukraine War: Average price **$2,200/oz** (76% above normal)
   - During COVID-19: Average price **$1,750/oz** (40% above normal)
   - Normal periods: Average **$1,250/oz**

2. **Neural Network is the recommended model:**
   - MAPE of 6.10% — best balance of accuracy and robustness
   - Can extrapolate beyond training range (unlike tree models)

3. **Linear Regression has lowest error but is misleading:**
   - 2.58% MAPE looks good but only because test period had a strong upward trend
   - Would fail badly during actual volatile periods

4. **Price_Lag1 is the most important feature** — gold prices have strong temporal autocorrelation

---

## 7. Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Language | Python 3.14 | Core development |
| Web Framework | Streamlit 1.58 | Interactive dashboard |
| ML Models | scikit-learn | LinearRegression, RandomForest, MLP |
| Boosting | XGBoost 3.3 | XGBRegressor |
| Data Processing | Pandas, NumPy | Manipulation, math |
| Visualization | Matplotlib 3.11 | Charts and graphs |
| Deployment | Streamlit Cloud | Free web hosting |
| Version Control | Git + GitHub | Code management |

---

## 8. Project Structure

```
gold_price_predictor/
    app.py              - Streamlit app (4 tabs orchestrator)
    train_models.py     - CLI script to train models + generate graphs
    generate_report.py  - Generates the PDF report
    requirements.txt    - Dependencies for deployment
    src/
        data_loader.py   - Loads CSV, cleans data, feature engineering
        models.py        - Trains and evaluates all 4 ML models
        visualization.py - Generates all charts (comparison, events, etc.)
        analysis.py      - Event statistics, forecasting, feature importance
    output/             - Generated graphs (PNG) and metrics (CSV/JSON)
```

---

## 9. Common Questions the Examiner Might Ask

### Q: Why not use LSTM / deep learning?
**A:** Python 3.14 does not have TensorFlow support yet. The Neural Network (MLP) in scikit-learn was used as an alternative. LSTM can be run on Google Colab and integrated in future work.

### Q: Why is Linear Regression's MAPE so low (2.58%)?
**A:** The test period (2021–2025) had a strong continuous upward trend. Linear Regression captures this well. However, it would perform poorly during volatile periods like COVID-19 or wars because it cannot model non-linear shocks.

### Q: Why did you use chronological split instead of random split?
**A:** In time-series data, random split causes data leakage — the model sees future patterns during training. Chronological split evaluates on truly unseen future data, giving realistic performance estimates.

### Q: What makes the Neural Network better than tree models?
**A:** Tree models (Random Forest, XGBoost) predict the average of training target values within leaf nodes. They cannot output values beyond their training range. Neural Networks use continuous activation functions that allow extrapolation beyond the training range.

### Q: How does the 6-month forecast work?
**A:** The model predicts month 1. That prediction becomes Price_Lag1 for month 2's prediction. The process repeats 6 times, feeding each prediction forward as input for the next month. This is called iterative/recursive forecasting.

### Q: Where did the data come from?
**A:** DataHub's Core Gold Prices dataset (open source). Monthly gold prices in USD per troy ounce from January 2000 to July 2025.

### Q: How is this different from the existing work (Almira's project)?
**A:** That project recommends business models for e-commerce using RF regressor. This project focuses on gold price prediction using 4 ML models + event impact analysis, deployed as an interactive Streamlit app with prediction and forecasting capabilities.

---

## 10. Limitations & Future Work

### Limitations
- Tree models cannot extrapolate beyond training range
- No real-time data — uses static CSV dataset
- TensorFlow/LSTM not supported on Python 3.14
- Only monthly frequency — daily data would give finer granularity

### Future Enhancements
- **Real-time data:** Integrate live gold price APIs
- **LSTM/Deep Learning:** Run on Google Colab for better sequential modeling
- **Sentiment Analysis:** Add news and social media sentiment via NLP
- **More data sources:** Currency rates, stock indices, geopolitical risk indices
- **Automated retraining:** Scheduled pipeline for periodic model updates
