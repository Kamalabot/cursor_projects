import joblib
import pandas as pd
import os
from datetime import datetime

class ModelHandler:
    def __init__(self, base_path='models/'):
        """Initialize with base path for model storage"""
        self.base_path = base_path
        self.create_directories()
        
    def create_directories(self):
        """Create necessary directories if they don't exist"""
        directories = ['prophet', 'sarima', 'xgboost', 'forecasts', 'data']
        for dir_name in directories:
            dir_path = os.path.join(self.base_path, dir_name)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                
    def save_model(self, model, model_type, store_number):
        """Save a trained model"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"store_{store_number}_{timestamp}.joblib"
        path = os.path.join(self.base_path, model_type, filename)
        
        try:
            if model_type == 'prophet':
                model.save(path)
            else:
                joblib.dump(model, path)
            print(f"Successfully saved {model_type} model for store {store_number}")
            return path
        except Exception as e:
            print(f"Error saving {model_type} model: {str(e)}")
            return None
            
    def save_forecast(self, forecast, model_type, store_number):
        """Save forecast results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"forecast_store_{store_number}_{timestamp}.csv"
        path = os.path.join(self.base_path, 'forecasts', filename)
        
        try:
            if isinstance(forecast, pd.DataFrame):
                forecast.to_csv(path, index=True)
            else:
                forecast.to_csv(path)
            print(f"Successfully saved {model_type} forecast for store {store_number}")
            return path
        except Exception as e:
            print(f"Error saving forecast: {str(e)}")
            return None
            
    def save_processed_data(self, data, store_number):
        """Save processed store data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"processed_data_store_{store_number}_{timestamp}.csv"
        path = os.path.join(self.base_path, 'data', filename)
        
        try:
            data.to_csv(path, index=False)
            print(f"Successfully saved processed data for store {store_number}")
            return path
        except Exception as e:
            print(f"Error saving processed data: {str(e)}")
            return None
            
    def load_model(self, model_path, model_type):
        """Load a saved model"""
        try:
            if model_type == 'prophet':
                from prophet import Prophet
                model = Prophet.load(model_path)
            else:
                model = joblib.load(model_path)
            print(f"Successfully loaded {model_type} model")
            return model
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            return None
            
    def load_forecast(self, forecast_path):
        """Load saved forecast results"""
        try:
            forecast = pd.read_csv(forecast_path)
            print("Successfully loaded forecast data")
            return forecast
        except Exception as e:
            print(f"Error loading forecast: {str(e)}")
            return None
            
    def load_processed_data(self, data_path):
        """Load saved processed data"""
        try:
            data = pd.read_csv(data_path)
            print("Successfully loaded processed data")
            return data
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return None
            
    def get_latest_model(self, model_type, store_number):
        """Get the most recent model for a specific store"""
        model_dir = os.path.join(self.base_path, model_type)
        files = [f for f in os.listdir(model_dir) if f.startswith(f"store_{store_number}_")]
        
        if not files:
            return None
            
        latest_file = max(files, key=lambda x: x.split('_')[2])
        return os.path.join(model_dir, latest_file)

# Example usage in the StoreSalesForecaster class: 