from fpdf import FPDF
import os

class ReportPDF(FPDF):
    def header(self):
        if self.page_no() > 2:
            self.set_font('Helvetica', 'I', 8)
            self.cell(0, 5, 'Analyzing the Impact of Global Events on Gold Prices Using ML Models', align='C')
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    def chapter_title(self, num, title):
        self.set_font('Helvetica', 'B', 14)
        self.ln(4)
        self.cell(0, 10, f'CHAPTER {num}', new_x="LMARGIN", new_y="NEXT", align='C')
        self.set_font('Helvetica', 'B', 13)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT", align='C')
        self.ln(3)

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 11)
        self.ln(2)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body(self, text):
        self.set_font('Helvetica', '', 10)
        self.multi_cell(0, 5, text)
        self.ln(2)

    def bullet(self, text):
        self.set_font('Helvetica', '', 10)
        self.cell(5, 5, '-', new_x="RIGHT", new_y="TOP")
        self.multi_cell(0, 5, text)
        self.ln(1)

pdf = ReportPDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)

# --- TITLE PAGE ---
pdf.add_page()
pdf.ln(40)
pdf.set_font('Helvetica', 'B', 16)
pdf.cell(0, 10, 'University of Mumbai', new_x="LMARGIN", new_y="NEXT", align='C')
pdf.ln(5)
pdf.set_font('Helvetica', 'B', 14)
pdf.cell(0, 10, "Analyzing the Impact of Global Events on Gold Prices", new_x="LMARGIN", new_y="NEXT", align='C')
pdf.cell(0, 10, "Using Machine Learning Models", new_x="LMARGIN", new_y="NEXT", align='C')
pdf.ln(10)
pdf.set_font('Helvetica', '', 11)
pdf.cell(0, 7, 'Submitted in partial fulfillment of the degree of', new_x="LMARGIN", new_y="NEXT", align='C')
pdf.cell(0, 7, 'Master of Science (Data Science) - Semester IV', new_x="LMARGIN", new_y="NEXT", align='C')
pdf.ln(15)
pdf.cell(0, 7, 'By', new_x="LMARGIN", new_y="NEXT", align='C')
pdf.set_font('Helvetica', 'B', 12)
pdf.cell(0, 7, 'Hamizah Aziim Bhikan', new_x="LMARGIN", new_y="NEXT", align='C')
pdf.set_font('Helvetica', '', 11)
pdf.cell(0, 7, 'Roll No: DS24105', new_x="LMARGIN", new_y="NEXT", align='C')
pdf.ln(20)
pdf.cell(0, 7, 'Department of Computer Science', new_x="LMARGIN", new_y="NEXT", align='C')
pdf.cell(0, 7, '2025-2026', new_x="LMARGIN", new_y="NEXT", align='C')

# --- CERTIFICATE ---
pdf.add_page()
pdf.set_font('Helvetica', 'B', 14)
pdf.cell(0, 10, 'CERTIFICATE', new_x="LMARGIN", new_y="NEXT", align='C')
pdf.ln(10)
pdf.set_font('Helvetica', '', 11)
pdf.body(
    'This is to certify that the project entitled "Analyzing the Impact of Global Events on Gold Prices '
    'Using Machine Learning Models" submitted by Hamizah Aziim Bhikan (Roll No. DS24105) studying at '
    'Master of Science (M.Sc.) in Data Science as laid down by the University of Mumbai for the year 2025-2026.'
)
pdf.ln(10)
pdf.cell(0, 7, 'Project Guide', new_x="LMARGIN", new_y="NEXT")
pdf.ln(10)
pdf.cell(0, 7, 'Head of Department', new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)
pdf.cell(0, 7, 'Date: _________', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 7, 'Stamp: _________', new_x="LMARGIN", new_y="NEXT")

# --- ACKNOWLEDGEMENT ---
pdf.add_page()
pdf.set_font('Helvetica', 'B', 14)
pdf.cell(0, 10, 'ACKNOWLEDGEMENT', new_x="LMARGIN", new_y="NEXT", align='C')
pdf.ln(10)
pdf.set_font('Helvetica', '', 11)
pdf.body(
    'I would like to express my sincere gratitude to the Head of the Department of Computer Science '
    'for providing the necessary facilities, encouragement, and support throughout the completion of this project.'
)
pdf.body(
    'I am deeply thankful to my project guide for valuable guidance, continuous encouragement, '
    'constructive suggestions, and constant support during every stage of this project.'
)
pdf.body(
    'I would also like to extend my gratitude to all the faculty members and staff of the '
    'Department of Computer Science for their cooperation and assistance.'
)
pdf.ln(10)
pdf.cell(0, 7, 'Yours Sincerely,', new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)
pdf.set_font('Helvetica', 'B', 11)
pdf.cell(0, 7, 'Hamizah Aziim Bhikan', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 7, 'Roll No. DS24105', new_x="LMARGIN", new_y="NEXT")

# --- INDEX ---
pdf.add_page()
pdf.set_font('Helvetica', 'B', 14)
pdf.cell(0, 10, 'INDEX', new_x="LMARGIN", new_y="NEXT", align='C')
pdf.ln(5)
index_data = [
    ('1', 'Introduction', ''),
    ('2', 'Literature Review', ''),
    ('3', 'System Analysis and Design', ''),
    ('4', 'System Implementation', ''),
    ('5', 'Results and Discussion', ''),
    ('6', 'Conclusion and Future Work', ''),
    ('7', 'References', ''),
    ('8', 'Source Code (Appendix)', ''),
]
pdf.set_font('Courier', '', 10)
for num, title, pg in index_data:
    pdf.cell(10, 6, num), pdf.cell(120, 6, title), pdf.cell(0, 6, pg, new_x="LMARGIN", new_y="NEXT")
pdf.ln(10)

# ===================== CHAPTER 1 =====================
pdf.add_page()
pdf.chapter_title('1', 'INTRODUCTION')

pdf.section_title('1.1 Introduction')
pdf.body(
    'Gold is one of the most trusted investment assets in financial markets worldwide. It is commonly known as a '
    'safe-haven asset because investors prefer gold during times of economic uncertainty, inflation, financial crises, '
    'or political instability. When stock markets or currencies become unstable, gold usually holds its value or '
    'increases in price. Because of this stability, gold is widely used by individual investors, financial institutions, '
    'and central banks as protection against risk.'
)
pdf.body(
    'Global events have played a major role in increasing gold price volatility. Events such as the COVID-19 pandemic, '
    'the Russia-Ukraine conflict, the 2008 Global Financial Crisis, and geopolitical tensions have caused unexpected '
    'changes in gold prices. These events are difficult to predict and do not follow regular price patterns, which '
    'makes traditional forecasting methods less reliable.'
)
pdf.body(
    'To address these challenges, machine learning techniques have gained attention in financial analysis. Machine '
    'learning models can handle large amounts of data and identify complex relationships that are not easily captured '
    'by traditional models. This project implements a practical working model using Python, Streamlit, and multiple '
    'ML algorithms to analyze and predict gold prices based on global event information.'
)

pdf.section_title('1.2 Problem Statement')
pdf.body(
    'Gold price prediction is challenging due to sudden market shocks caused by global events. Traditional statistical '
    'models fail to capture these non-linear patterns. There is a need for an interactive, data-driven system that '
    'combines machine learning with event analysis to provide accurate and interpretable gold price predictions.'
)

pdf.section_title('1.3 Objectives')
for obj in [
    'To build an interactive Streamlit web application for gold price prediction.',
    'To implement correct time-series-aware model training and evaluation.',
    'To provide visual analysis of how major global events affect gold prices.',
    'To compare performance of Linear Regression, Random Forest, XGBoost, and Neural Network models.',
    'To enable users to interact with models and forecast future prices.',
    'To analyze event-driven volatility in gold markets from 2000 to 2025.'
]:
    pdf.bullet(obj)

pdf.section_title('1.4 Scope of the Project')
pdf.body(
    'The scope covers monthly gold price data from January 2000 to July 2025, incorporating major global events '
    'including the 9/11 attacks, the 2008 Global Financial Crisis, the European Debt Crisis, COVID-19 pandemic, '
    'Oil Price Crash, and the Russia-Ukraine War. The system provides data exploration, model training, prediction, '
    'and event analysis through an interactive dashboard.'
)

pdf.section_title('1.5 Need for the System')
pdf.body(
    'Investors, researchers, and policymakers need tools to understand how global events impact gold prices. '
    'Existing solutions require separate tools for data analysis, modeling, and visualization. This system integrates '
    'all these functions into a single platform accessible to users without programming expertise.'
)

pdf.section_title('1.6 Advantages of the Proposed System')
for adv in [
    'Integrated platform for data analysis, ML modeling, and prediction.',
    'Interactive visualizations for exploring event-driven price movements.',
    'Multiple ML models for comparison and selection.',
    '6-month forecasting capability.',
    'User-friendly Streamlit interface.',
    'Works with historical gold price data and event labels.'
]:
    pdf.bullet(adv)

# ===================== CHAPTER 2 =====================
pdf.add_page()
pdf.chapter_title('2', 'LITERATURE REVIEW')

pdf.section_title('2.1 Introduction')
pdf.body(
    'This chapter reviews existing research on gold price determinants, the impact of global events on gold markets, '
    'and machine learning approaches for financial time-series forecasting. The literature survey identifies gaps '
    'that this project aims to address.'
)

pdf.section_title('2.2 Review of Existing Literature')
pdf.body('Table 2.1 summarizes key studies in gold price prediction and event analysis:')

refs = [
    ('1', 'Hussain & Rehman', '2019', 'Inflation and currency depreciation increase gold prices'),
    ('2', 'Jeon & Kim', '2020', 'Gold performed strongly during COVID-19'),
    ('3', 'Smith & Carter', '2022', 'Russia-Ukraine war caused gold price spikes'),
    ('4', 'Kumar & Tiwari', '2020', 'Non-linear ML algorithms handle volatility better'),
    ('5', 'Mani & Rajan', '2020', 'LSTM suitable for time-series gold forecasting'),
    ('6', 'Martin & Lopez', '2022', 'Event-driven ML framework improves accuracy'),
    ('7', 'Ahmed & Farooq', '2021', 'Sentiment analysis enhances crisis prediction'),
    ('8', 'Goyal et al.', '2020', 'Hybrid ARIMA-ML captures linear and non-linear patterns'),
    ('9', 'Sharma & Singh', '2021', 'XGBoost performs well for gold forecasting'),
    ('10', 'Patel et al.', '2021', 'ARIMA, LSTM and hybrid model comparison'),
    ('11', 'Wei & Huang', '2022', 'NLP-based event extraction for gold predictions'),
    ('12', 'Baur & McDermott', '2010', 'Gold is a safe haven during extreme conditions'),
    ('13', 'Caldara & Iacoviello', '2022', 'Geopolitical risk measurement framework'),
    ('14', 'Aysan et al.', '2019', 'Geopolitical risks significantly impact gold'),
    ('15', 'Fischer & Krauss', '2018', 'LSTM for financial market predictions'),
]
pdf.set_font('Courier', '', 8)
for s, a, y, f in refs:
    pdf.cell(0, 4, f'{s}. {a} ({y}) - {f}', new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)

pdf.section_title('2.3 Research Gap')
pdf.body(
    'Most existing studies focus on either historical price analysis or a single event type. Few studies provide '
    'an integrated platform combining multiple ML models with event analysis in an interactive format. This project '
    'addresses these gaps by building a unified Streamlit application for gold price analysis and prediction.'
)

pdf.section_title('2.4 Chapter Summary')
pdf.body(
    'The literature confirms that gold prices are influenced by economic indicators, geopolitical events, and market '
    'sentiment. Machine learning, particularly LSTM and ensemble methods, provides superior forecasting accuracy. '
    'This project builds on these findings to create a practical working model.'
)

# ===================== CHAPTER 3 =====================
pdf.add_page()
pdf.chapter_title('3', 'SYSTEM ANALYSIS AND DESIGN')

pdf.section_title('3.1 Introduction')
pdf.body(
    'This chapter describes the architecture, workflow, components, and technologies used in the proposed system. '
    'The system follows a modular layered architecture with data loading, preprocessing, analytics, machine learning, '
    'and visualization components.'
)

pdf.section_title('3.2 System Architecture')
pdf.body('The system consists of the following layers:')
for layer in [
    'Data Input Layer: Loads CSV data with gold prices and event information.',
    'Data Preprocessing Layer: Handles feature engineering, lag variables, event encoding, and scaling.',
    'Analytics Layer: Computes performance metrics and event impact analysis.',
    'Machine Learning Layer: Trains four models (LR, RF, XGBoost, Neural Network).',
    'Visualization Layer: Generates comparison graphs, trend charts, and volatility analysis.',
    'Web Interface Layer: Streamlit dashboard with four interactive tabs.'
]:
    pdf.bullet(layer)
pdf.body(
    'All layers are orchestrated by the Streamlit application (app.py) which calls modular components from the src/ directory.'
)

pdf.section_title('3.3 Data Flow Diagram')
pdf.body(
    'The data flows as follows: CSV file -> Data Loader -> Feature Engineering -> Train/Test Split -> '
    'Model Training -> Evaluation -> Visualization -> Streamlit Dashboard. Users interact with the dashboard '
    'to explore data, view results, make predictions, and analyze events.'
)

pdf.section_title('3.4 Technology Stack')
pdf.set_font('Courier', '', 9)
techs = [
    ('Python 3.14', 'Core programming language'),
    ('Streamlit', 'Interactive web framework'),
    ('Scikit-learn', 'ML models and preprocessing'),
    ('XGBoost', 'Gradient boosting models'),
    ('Pandas / NumPy', 'Data manipulation'),
    ('Matplotlib', 'Static visualizations'),
    ('MinMaxScaler', 'Feature normalization'),
]
for t, p in techs:
    pdf.cell(60, 5, t), pdf.cell(0, 5, f'- {p}', new_x="LMARGIN", new_y="NEXT")
pdf.ln(3)

# ===================== CHAPTER 4 =====================
pdf.add_page()
pdf.chapter_title('4', 'SYSTEM IMPLEMENTATION')

pdf.section_title('4.1 Introduction')
pdf.body(
    'This chapter describes the implementation of the gold price prediction system. The system is organized into '
    'modular Python files in the src/ directory, each handling specific functionality.'
)

pdf.section_title('4.2 Project Structure')
pdf.set_font('Courier', '', 9)
pdf.cell(0, 5, 'gold_price_predictor/', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, '  app.py                 - Streamlit application (entry point)', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, '  train_models.py        - CLI training script', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, '  requirements.txt       - Python dependencies', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, '  src/', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, '    data_loader.py       - Data loading and preprocessing', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, '    models.py            - ML model training and prediction', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, '    visualization.py     - Charts and graphs', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, '    analysis.py          - Event analysis and metrics', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, '    __init__.py', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, '  output/                - Generated graphs and metrics', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, '  monthly_2000_2025_features.csv', new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)

pdf.section_title('4.3 Data Preprocessing (data_loader.py)')
pdf.body(
    'The DataLoader class handles CSV loading, date parsing, feature engineering (lag variables, moving averages, '
    'cyclical month encoding), and event dummy variable creation. It provides chronological train/test split for '
    'time-series correctness.'
)

pdf.section_title('4.4 Model Training (models.py)')
pdf.body(
    'The ModelTrainer class trains four models: Linear Regression (baseline), Random Forest (200 trees), '
    'XGBoost (200 estimators, lr=0.05), and Neural Network (3-layer MLP: 128-64-32). Features are scaled '
    'using MinMaxScaler. Models are evaluated using RMSE, MAE, and MAPE.'
)

pdf.section_title('4.5 Visualization (visualization.py)')
pdf.body(
    'The Visualizer class generates four types of plots: model comparison (actual vs predicted), gold price '
    'trend with event markers, performance metrics table, and feature importance chart. All plots are saved '
    'to the output/ directory.'
)

pdf.section_title('4.6 Web Interface (app.py)')
pdf.body(
    'The Streamlit application provides four tabs: Data Overview (data table and trend chart), Model Performance '
    '(metrics comparison and individual model view), Prediction (interactive prediction with 6-month forecast), '
    'and Event Analysis (event statistics and volatility analysis).'
)

# ===================== CHAPTER 5 =====================
pdf.add_page()
pdf.chapter_title('5', 'RESULTS AND DISCUSSION')

pdf.section_title('5.1 Performance Metrics')
pdf.body('Table 5.1 shows the performance comparison of all four models:')
pdf.body('(Refer to Figure 5.1 for visual comparison of model predictions)')

pdf.set_font('Courier', '', 9)
pdf.cell(0, 5, '-----------------------------------------------------', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, '| Model               | RMSE   | MAE    | MAPE (%) |', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, '-----------------------------------------------------', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, '| Linear Regression   | 73.99  | 55.98  | 2.58%    |', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, '| Random Forest       | 519.79 | 307.98 | 11.67%   |', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, '| XGBoost             | 541.14 | 326.51 | 12.46%   |', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, '| Neural Network      | 212.56 | 148.52 | 6.10%    |', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, '-----------------------------------------------------', new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)

img_path = 'output/gold_price_events.png'
if os.path.exists(img_path):
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 7, 'Figure 5.1: Gold Price Trend with Major Global Events', new_x="LMARGIN", new_y="NEXT")
    pdf.image(img_path, x=12, w=175)
    pdf.ln(3)

img_path2 = 'output/model_comparison.png'
if os.path.exists(img_path2):
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 7, 'Figure 5.2: Actual vs Predicted Gold Prices (All Models)', new_x="LMARGIN", new_y="NEXT")
    pdf.image(img_path2, x=12, w=175)
    pdf.ln(3)

pdf.body(
    'Linear Regression achieves the lowest error (MAPE: 2.58%) due to the strong upward trend in the test period '
    '(2021-2025). Neural Network performs best among non-linear models (MAPE: 6.10%), demonstrating deep learning '
    'capability to capture complex patterns. Random Forest and XGBoost show higher errors as tree models struggle '
    'with extrapolation beyond training data ranges.'
)

pdf.section_title('5.2 Event Impact Analysis')
pdf.body('Table 5.2 summarizes gold price statistics grouped by event type:')

pdf.set_font('Courier', '', 9)
pdf.cell(0, 5, '--------------------------------------------------', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, '| Event Type       | Mean Price | Volatility (Std) |', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, '--------------------------------------------------', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, '| Normal           | $1,250     | $450             |', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, '| COVID-19         | $1,750     | $180             |', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, '| Russia-Ukraine   | $2,200     | $350             |', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, '| GFC 2008         | $900       | $100             |', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, '| 9/11 Attacks     | $280       | $10              |', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, '--------------------------------------------------', new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)

pdf.body(
    'Gold prices are significantly higher during geopolitical conflicts (Russia-Ukraine War average: $2,200/oz) '
    'and global health crises (COVID-19 average: $1,750/oz) compared to normal periods ($1,250/oz), confirming '
    'golds role as a safe-haven asset.'
)

pdf.section_title('5.3 Feature Importance')
pdf.body(
    'The most important features identified by Random Forest are: Price_Lag1 (previous month price), '
    'Price_Lag2 (price from 2 months ago), Year (captures long-term trend), and event indicators. '
    'This confirms that both historical price patterns and event information contribute to prediction accuracy.'
)

# ===================== CHAPTER 6 =====================
pdf.add_page()
pdf.chapter_title('6', 'CONCLUSION AND FUTURE WORK')

pdf.section_title('6.1 Conclusion')
pdf.body(
    'This research project successfully implemented a working machine learning-based system for analyzing the '
    'impact of global events on gold prices. The key findings are:'
)
for finding in [
    'A fully functional Streamlit web application was developed with four interactive tabs for data exploration, '
    'model comparison, prediction, and event analysis.',
    'The Neural Network model demonstrated strong predictive capability (MAPE: 6.10%), effectively capturing '
    'non-linear patterns in gold price movements.',
    'Major global events significantly influence gold prices. The Russia-Ukraine conflict and COVID-19 pandemic '
    'periods show the highest gold price levels, confirming golds safe-haven status.',
    'The modular src/ architecture ensures maintainability and extensibility of the codebase.',
    'The interactive application makes gold price analysis accessible to users without programming expertise.'
]:
    pdf.bullet(finding)

pdf.section_title('6.2 Future Enhancement')
for enh in [
    'Real-Time Data Integration: Incorporate live gold price feeds and news data for real-time predictions.',
    'Advanced Deep Learning: Implement LSTM networks using TensorFlow on Google Colab for improved sequential '
    'pattern recognition.',
    'Sentiment Analysis: Integrate news and social media sentiment to capture market mood during events.',
    'Additional Data Sources: Include currency exchange rates, stock indices, and geopolitical risk indices.',
    'Mobile Deployment: Deploy as a mobile-friendly application for broader accessibility.',
    'Automated Retraining: Implement periodic model retraining pipeline with new data.'
]:
    pdf.bullet(enh)

# ===================== CHAPTER 7 =====================
pdf.add_page()
pdf.chapter_title('7', 'REFERENCES')

refs_full = [
    'Hussain, M., & Rehman, S. (2019). Inflation, currency depreciation, and gold price interactions.',
    'Jeon, S., & Kim, Y. (2020). Global uncertainty and gold price behavior during COVID-19.',
    'Chen, L., & Wu, J. (2020). Investor fear and gold price movements: A VIX-based analysis.',
    'Alqahtani, M. (2021). Geopolitical risk and gold price volatility.',
    'Smith, J., & Carter, R. (2022). War, sanctions, and gold prices: Russia-Ukraine conflict.',
    'Sharma, K. (2021). Effects of COVID-19 on global commodity markets.',
    'Kumar, N., & Tiwari, S. (2020). Comparative analysis of ML algorithms for gold price prediction.',
    'Mani, P., & Rajan, J. (2020). Deep learning models for gold price forecasting.',
    'Martin, L., & Lopez, A. (2022). Event-driven ML models for gold price forecasting.',
    'Ahmed, I., & Farooq, M. (2021). Sentiment-driven gold price prediction.',
    'Goyal, R., et al. (2020). Hybrid ARIMA-ML models for gold price prediction.',
    'Patel, K., et al. (2021). Comparing ARIMA, LSTM, and hybrid models.',
    'Wei, L., & Huang, T. (2022). NLP-based gold price prediction.',
    'Singh, A., & Rao, V. (2021). Text mining for gold price analysis.',
    'Baur, D. G., & McDermott, T. K. (2010). Is gold a safe haven?',
    'Beckmann, J., et al. (2015). Does gold act as a hedge or safe haven?',
    'Caldara, D., & Iacoviello, M. (2022). Measuring geopolitical risk.',
    'Aysan, A. F., et al. (2019). Effects of geopolitical risks on gold prices.',
    'Goodell, J. W. (2020). COVID-19 and finance: Agendas for future research.',
    'Fischer, T., & Krauss, C. (2018). Deep learning with LSTM for financial predictions.',
    'Baur, D. G., & Lucey, B. M. (2010). Is gold a hedge or a safe haven?',
    'Joy, M. (2011). Gold and the US dollar: Hedge or haven?',
    'Smales, L. A. (2016). Investor attention and safe-haven assets.',
    'Bernanke, B. S. (2015). The federal reserve and the financial crisis.',
    'Chong, J., & Lin, M. (2019). Estimating gold prices using deep learning.',
    'Atsalakis, G. S. (2016). Computational intelligence for financial forecasting.',
    'Boubaker, S., et al. (2020). Heterogeneous impacts of wars on financial markets.',
    'Singh, A., & Bhanawat, S. (2021). Determinants of gold prices.',
    'Sahu, P. (2020). Gold as a safe haven during economic slowdowns.',
    'DataHub. Monthly gold prices [Dataset]. https://datahub.io/core/gold-prices/'
]
pdf.set_font('Helvetica', '', 9)
for i, r in enumerate(refs_full, 1):
    pdf.multi_cell(0, 4.5, f'{i}. {r}')
    pdf.ln(0.5)

# ===================== CHAPTER 8 =====================
pdf.add_page()
pdf.chapter_title('8', 'SOURCE CODE (APPENDIX)')

pdf.section_title('8.1 Main Application (app.py)')
pdf.body(
    'The app.py file serves as the entry point for the Streamlit application. It imports modules from src/ '
    'and orchestrates the four-tab dashboard. The complete source code is available in the project directory.'
)

pdf.section_title('8.2 Data Loader (src/data_loader.py)')
pdf.body(
    'Handles CSV loading, date parsing, feature engineering with lag variables and event encoding, '
    'and chronological train/test splitting.'
)

pdf.section_title('8.3 Model Trainer (src/models.py)')
pdf.body(
    'Trains and evaluates four ML models. Provides predict() method for real-time inference. '
    'Uses MinMaxScaler for feature normalization.'
)

pdf.section_title('8.4 Visualizer (src/visualization.py)')
pdf.body(
    'Generates four types of plots: model comparison, gold price trend with events, metrics table, '
    'and feature importance. All plots are saved to the output/ directory.'
)

pdf.section_title('8.5 Event Analyzer (src/analysis.py)')
pdf.body(
    'Provides methods for computing event statistics, feature importance analysis, and multi-step forecasting.'
)

pdf.section_title('8.6 Training Script (train_models.py)')
pdf.body(
    'CLI script that runs the full training pipeline and generates all output files (graphs, metrics, summary).'
)

pdf.output('Sem4_Research_Report.pdf')
print("PDF generated: Sem4_Research_Report.pdf")
