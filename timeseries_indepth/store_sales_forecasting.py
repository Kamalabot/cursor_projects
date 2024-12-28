import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
from prophet import Prophet
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings
from store_sales_preprocessing import StoreSalesPreprocessor
from store_sales_model_handler import ModelHandler
warnings.filterwarnings('ignore')

class StoreSalesForecaster:
    def __init__(self):
        self.preprocessor = StoreSalesPreprocessor()
        self.scaler = StandardScaler()
        self.model_handler = ModelHandler()
        
    def prepare_store_data(self, store_number):
        """Prepare data for a specific store"""
        self.preprocessor.load_data(base_path='store-sales-time-series-forecasting/')
        self.preprocessor.process_data()
        return self.preprocessor.get_store_data(store_number)
    
    def train_test_split(self, data, test_days=30):
        """Split data into training and testing sets"""
        split_date = data['date'].max() - pd.Timedelta(days=test_days)
        train = data[data['date'] <= split_date]
        test = data[data['date'] > split_date]
        return train, test
    
    def prepare_prophet_data(self, store_data):
        """Prepare data specifically for Prophet"""
        # Select only required columns and rename them
        prophet_data = store_data[['date', 'sales']].copy()
        prophet_data.columns = ['ds', 'y']
        
        # Ensure no missing values
        prophet_data = prophet_data.dropna()
        
        # Convert date to datetime if not already
        prophet_data['ds'] = pd.to_datetime(prophet_data['ds'])
        
        return prophet_data
    
    def prophet_forecast(self, store_data, forecast_days=30):
        """Forecast using Facebook Prophet with proper error handling"""
        try:
            print("Preparing data for Prophet...")
            prophet_data = self.prepare_prophet_data(store_data)
            
            print("Initializing Prophet model...")
            model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=True,
                daily_seasonality=False,
                seasonality_mode='multiplicative',
                interval_width=0.95
            )
            
            print("Training Prophet model...")
            model.fit(prophet_data)
            
            print("Generating future dates...")
            future_dates = model.make_future_dataframe(
                periods=forecast_days,
                freq='D'
            )
            
            print("Making predictions...")
            forecast = model.predict(future_dates)
            
            # Select only necessary columns
            forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
            
            print("Prophet forecast completed successfully")
            return model, forecast
            
        except Exception as e:
            print(f"Error in Prophet forecasting: {str(e)}")
            raise
    
    def sarima_forecast(self, store_data, forecast_days=30):
        """Forecast using SARIMA model"""
        print("Training SARIMA model...")
        
        # Prepare data
        data = store_data.set_index('date')['sales']
        
        # Fit SARIMA model
        model = SARIMAX(
            data,
            order=(1, 1, 1),
            seasonal_order=(1, 1, 1, 7)
        )
        results = model.fit()
        
        # Generate forecast
        forecast = results.forecast(steps=forecast_days)
        return results, forecast
    
    def xgboost_forecast(self, store_data, forecast_days=30):
        """Forecast using XGBoost"""
        print("Training XGBoost model...")
        
        # Prepare features
        features = ['year', 'month', 'day', 'day_of_week', 'is_weekend',
                   'dcoilwtico', 'transactions', 'is_holiday']
        
        # Split data
        train, test = self.train_test_split(store_data, forecast_days)
        
        # Scale features
        X_train = self.scaler.fit_transform(train[features])
        y_train = train['sales']
        
        # Train model
        model = xgb.XGBRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=7
        )
        model.fit(X_train, y_train)
        
        # Prepare test features
        X_test = self.scaler.transform(test[features])
        
        # Generate forecast
        forecast = pd.Series(
            model.predict(X_test),
            index=test.index
        )
        return model, forecast
    
    def evaluate_forecast(self, actual, predicted):
        """Calculate forecast evaluation metrics"""
        rmse = np.sqrt(mean_squared_error(actual, predicted))
        mae = mean_absolute_error(actual, predicted)
        mape = np.mean(np.abs((actual - predicted) / actual)) * 100
        
        return {
            'RMSE': rmse,
            'MAE': mae,
            'MAPE': mape
        }
    
    def plot_forecasts(self, store_data, prophet_forecast, sarima_forecast, xgb_forecast):
        """Plot actual vs forecasted values with error handling"""
        try:
            import matplotlib.pyplot as plt
            
            # Convert dates to pandas datetime
            end_date = pd.to_datetime(store_data['date'].max()) + pd.Timedelta(days=30)
            start_date = end_date - pd.Timedelta(days=90)
            
            # Filter actual data
            recent_actual = store_data[
                (pd.to_datetime(store_data['date']) >= start_date) & 
                (pd.to_datetime(store_data['date']) <= end_date)
            ]
            
            plt.figure(figsize=(15, 8))
            
            # Plot actual values
            plt.plot(recent_actual['date'], recent_actual['sales'], 
                    label='Actual', color='black', linewidth=2)
            
            # Plot Prophet forecast if available
            if prophet_forecast is not None:
                prophet_recent = prophet_forecast[
                    (pd.to_datetime(prophet_forecast['ds']) >= start_date) & 
                    (pd.to_datetime(prophet_forecast['ds']) <= end_date)
                ]
                plt.plot(prophet_recent['ds'], prophet_recent['yhat'], 
                        label='Prophet', color='blue', linestyle='--')
                
                # Add confidence intervals
                plt.fill_between(
                    prophet_recent['ds'],
                    prophet_recent['yhat_lower'],
                    prophet_recent['yhat_upper'],
                    color='blue', alpha=0.1
                )
            
            # Plot SARIMA forecast if available
            if sarima_forecast is not None:
                sarima_recent = sarima_forecast[
                    (sarima_forecast.index >= start_date) & 
                    (sarima_forecast.index <= end_date)
                ]
                plt.plot(sarima_recent.index, sarima_recent.values, 
                        label='SARIMA', color='red', linestyle='--')
            
            # Plot XGBoost forecast if available
            if xgb_forecast is not None:
                xgb_recent = xgb_forecast[
                    (xgb_forecast.index >= start_date) & 
                    (xgb_forecast.index <= end_date)
                ]
                plt.plot(xgb_recent.index, xgb_recent.values, 
                        label='XGBoost', color='green', linestyle='--')
            
            plt.title('Store Sales Forecast Comparison')
            plt.xlabel('Date')
            plt.ylabel('Sales')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            print(f"Error in plotting forecasts: {str(e)}")
            raise

    def save_models_and_forecasts(self, store_number, prophet_model, sarima_model, 
                                xgb_model, prophet_forecast, sarima_forecast, 
                                xgb_forecast, store_data):
        """Save all models and forecasts"""
        # Save models
        self.model_handler.save_model(prophet_model, 'prophet', store_number)
        self.model_handler.save_model(sarima_model, 'sarima', store_number)
        self.model_handler.save_model(xgb_model, 'xgboost', store_number)
        
        # Save forecasts
        self.model_handler.save_forecast(prophet_forecast, 'prophet', store_number)
        self.model_handler.save_forecast(sarima_forecast, 'sarima', store_number)
        self.model_handler.save_forecast(xgb_forecast, 'xgboost', store_number)
        
        # Save processed data
        self.model_handler.save_processed_data(store_data, store_number)

def main():
    try:
        # Initialize forecaster
        forecaster = StoreSalesForecaster()
        
        # Prepare data for a specific store (e.g., store 1)
        store_number = 1
        print(f"Preparing data for store {store_number}...")
        store_data = forecaster.prepare_store_data(store_number)
        
        # Generate forecasts
        forecast_days = 30
        
        # Prophet forecast
        print("\nGenerating Prophet forecast...")
        prophet_model, prophet_forecast = forecaster.prophet_forecast(store_data, forecast_days)
        
        # SARIMA forecast
        print("\nGenerating SARIMA forecast...")
        sarima_model, sarima_forecast = forecaster.sarima_forecast(store_data, forecast_days)
        
        # XGBoost forecast
        print("\nGenerating XGBoost forecast...")
        xgb_model, xgb_forecast = forecaster.xgboost_forecast(store_data, forecast_days)
        
        # Save models and forecasts
        print("\nSaving models and forecasts...")
        forecaster.model_handler.save_models_and_forecasts(
            store_number,
            prophet_model,
            sarima_model,
            xgb_model,
            prophet_forecast,
            sarima_forecast,
            xgb_forecast,
            store_data
        )
        
        # Plot results
        print("\nPlotting forecasts...")
        forecaster.plot_forecasts(store_data, prophet_forecast, sarima_forecast, xgb_forecast)
        
    except Exception as e:
        print(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main() 