import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

class ModelTrainer:
    def __init__(self):
        self.scaler_X = MinMaxScaler()
        self.scaler_y = MinMaxScaler()
        self.lr_scaler_X = MinMaxScaler()
        self.trained_models = {}
        self.results = {}

    def train(self, data_dict):
        X_train, y_train = data_dict['X_train'], data_dict['y_train']
        X_test, y_test = data_dict['X_test'], data_dict['y_test']
        lr_X_train, lr_X_test = data_dict['lr_X_train'], data_dict['lr_X_test']

        X_train_s = self.scaler_X.fit_transform(X_train)
        X_test_s = self.scaler_X.transform(X_test)
        lr_X_train_s = self.lr_scaler_X.fit_transform(lr_X_train)
        lr_X_test_s = self.lr_scaler_X.transform(lr_X_test)
        y_train_s = self.scaler_y.fit_transform(y_train.reshape(-1, 1)).ravel()
        y_test_s = self.scaler_y.transform(y_test.reshape(-1, 1)).ravel()

        lr = LinearRegression()
        lr.fit(lr_X_train_s, y_train_s)
        self.trained_models['Linear Regression'] = (lr, lr_X_test_s, self.lr_scaler_X, 'lr')

        rf = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
        rf.fit(X_train_s, y_train_s)
        self.trained_models['Random Forest'] = (rf, X_test_s, self.scaler_X, 'full')

        xgb = XGBRegressor(n_estimators=200, learning_rate=0.05, random_state=42, verbosity=0)
        xgb.fit(X_train_s, y_train_s)
        self.trained_models['XGBoost'] = (xgb, X_test_s, self.scaler_X, 'full')

        nn = MLPRegressor(hidden_layer_sizes=(128, 64, 32), activation='relu',
                          solver='adam', max_iter=500, random_state=42, early_stopping=True)
        nn.fit(X_train_s, y_train_s)
        self.trained_models['Neural Network'] = (nn, X_test_s, self.scaler_X, 'full')

        self.results = {}
        for name, (model, test_s, _, _) in self.trained_models.items():
            y_pred_s = model.predict(test_s)
            y_pred = self.scaler_y.inverse_transform(y_pred_s.reshape(-1, 1)).flatten()
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            mae = mean_absolute_error(y_test, y_pred)
            mape = np.mean(np.abs((y_test - y_pred) / (y_test + 1e-8))) * 100
            self.results[name] = {
                'RMSE': round(rmse, 2),
                'MAE': round(mae, 2),
                'MAPE': round(mape, 2),
                'predictions': y_pred
            }

        return self.results

    def predict(self, model_name, input_dict, feature_cols, lr_features):
        if model_name == 'Linear Regression':
            model, _, scaler, _ = self.trained_models[model_name]
            inp = pd.DataFrame([input_dict])
            inp = inp[[c for c in lr_features if c in inp.columns]]
            for c in lr_features:
                if c not in inp.columns:
                    inp[c] = 0
            scaled = scaler.transform(inp[lr_features].values)
            pred_s = model.predict(scaled)
        else:
            model, _, scaler, _ = self.trained_models[model_name]
            inp = pd.DataFrame([input_dict])[feature_cols]
            scaled = scaler.transform(inp.values)
            pred_s = model.predict(scaled)
        return self.scaler_y.inverse_transform(pred_s.reshape(-1, 1))[0][0]


