import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

class StoreSalesPreprocessor:
    def __init__(self):
        self.train_df = None
        self.stores_df = None
        self.oil_df = None
        self.holidays_df = None
        self.transactions_df = None
        
    def load_data(self, base_path=''):
        """Load all necessary datasets"""
        print("Loading datasets...")
        self.train_df = pd.read_csv(f'{base_path}train.csv')
        self.stores_df = pd.read_csv(f'{base_path}stores.csv')
        self.oil_df = pd.read_csv(f'{base_path}oil.csv')
        self.holidays_df = pd.read_csv(f'{base_path}holidays_events.csv')
        self.transactions_df = pd.read_csv(f'{base_path}transactions.csv')
        
    def clean_dates(self):
        """Convert date columns to datetime"""
        print("Converting dates...")
        self.train_df['date'] = pd.to_datetime(self.train_df['date'])
        self.oil_df['date'] = pd.to_datetime(self.oil_df['date'])
        self.holidays_df['date'] = pd.to_datetime(self.holidays_df['date'])
        self.transactions_df['date'] = pd.to_datetime(self.transactions_df['date'])
        
    def handle_missing_values(self):
        """Handle missing values in all datasets"""
        print("Handling missing values...")
        
        # Fill missing oil prices using forward fill method
        self.oil_df['dcoilwtico'] = self.oil_df['dcoilwtico'].fillna(method='ffill')
        
        # Create a complete date range for oil prices
        date_range = pd.date_range(start=self.train_df['date'].min(),
                                 end=self.train_df['date'].max(),
                                 freq='D')
        
        complete_oil_df = pd.DataFrame({'date': date_range})
        self.oil_df = pd.merge(complete_oil_df, self.oil_df, on='date', how='left')
        self.oil_df['dcoilwtico'] = self.oil_df['dcoilwtico'].fillna(method='ffill')
        
    def create_features(self):
        """Create time-based and additional features"""
        print("Creating features...")
        
        # Time-based features
        self.train_df['year'] = self.train_df['date'].dt.year
        self.train_df['month'] = self.train_df['date'].dt.month
        self.train_df['day'] = self.train_df['date'].dt.day
        self.train_df['day_of_week'] = self.train_df['date'].dt.dayofweek
        self.train_df['is_weekend'] = self.train_df['day_of_week'].isin([5, 6]).astype(int)
        
        # Add store information
        self.train_df = self.train_df.merge(self.stores_df, on='store_nbr', how='left')
        
        # Add oil prices
        self.train_df = self.train_df.merge(self.oil_df[['date', 'dcoilwtico']], 
                                          on='date', 
                                          how='left')
        
        # Add transactions
        self.train_df = self.train_df.merge(self.transactions_df, 
                                          on=['date', 'store_nbr'], 
                                          how='left')
        
        # Process holidays
        self.process_holidays()
        
    def process_holidays(self):
        """Process and add holiday information"""
        print("Processing holidays...")
        
        # Create holiday features
        holidays_processed = self.holidays_df.copy()
        holidays_processed['is_holiday'] = 1
        holidays_processed['is_transferred'] = holidays_processed['type'] == 'Transfer'
        
        # Merge holidays with main dataset
        self.train_df = self.train_df.merge(
            holidays_processed[['date', 'is_holiday', 'is_transferred']],
            on='date',
            how='left'
        )
        
        # Fill missing holiday indicators with 0
        self.train_df['is_holiday'] = self.train_df['is_holiday'].fillna(0)
        self.train_df['is_transferred'] = self.train_df['is_transferred'].fillna(0)
        
    def remove_outliers(self, zscore_threshold=3):
        """Remove extreme outliers based on z-score"""
        print("Handling outliers...")
        
        # Calculate z-scores for sales by store and family
        self.train_df['sales_zscore'] = self.train_df.groupby(['store_nbr', 'family'])['sales'].transform(
            lambda x: (x - x.mean()) / x.std()
        )
        
        # Remove extreme outliers
        self.train_df = self.train_df[abs(self.train_df['sales_zscore']) < zscore_threshold]
        self.train_df.drop('sales_zscore', axis=1, inplace=True)
        
    def get_store_data(self, store_number):
        """Get processed data for a specific store"""
        return self.train_df[self.train_df['store_nbr'] == store_number].copy()
    
    def process_data(self):
        """Run all preprocessing steps"""
        self.clean_dates()
        self.handle_missing_values()
        self.create_features()
        self.remove_outliers()
        
        print("\nData processing completed!")
        print(f"Final dataset shape: {self.train_df.shape}")
        return self.train_df

def main():
    # Initialize preprocessor
    preprocessor = StoreSalesPreprocessor()
    
    # Load and process data
    preprocessor.load_data(base_path='store-sales-time-series-forecasting/')
    processed_data = preprocessor.process_data()
    
    # Example: Get data for store #1
    store_1_data = preprocessor.get_store_data(1)
    
    # Display sample of processed data
    print("\nSample of processed data for Store #1:")
    print(store_1_data.head())
    
    # Basic visualization for store 1
    plt.figure(figsize=(15, 6))
    store_1_data.groupby('date')['sales'].sum().plot()
    plt.title('Daily Sales for Store #1')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.show()

if __name__ == "__main__":
    main() 