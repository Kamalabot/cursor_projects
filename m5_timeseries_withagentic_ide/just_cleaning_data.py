import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

# Load the datasets
calendar_df = pd.read_csv('m5-forecasting-accuracy/calendar.csv')
sales_train_validation_df = pd.read_csv('m5-forecasting-accuracy/sales_train_validation.csv')
sell_prices_df = pd.read_csv('m5-forecasting-accuracy/sell_prices.csv')

def clean_calendar_data(df):
    """Clean calendar dataset"""
    print("Cleaning calendar data...")
    
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Combine event_name_1 and event_name_2 into a single 'events' column
    # Strategy: If both events exist, combine them with semicolon
    df['events'] = df['event_name_1'].fillna('') + df.apply(lambda x: ';' + x['event_name_2'] if pd.notna(x['event_name_2']) else '', axis=1)
    df['events'] = df['events'].replace('', np.nan)
    
    # Create binary columns for event types
    df['has_holiday'] = df['event_type_1'].notna().astype(int)
    df['is_national_holiday'] = ((df['event_type_1'] == 'National') | (df['event_type_2'] == 'National')).astype(int)
    df['is_religious_holiday'] = ((df['event_type_1'] == 'Religious') | (df['event_type_2'] == 'Religious')).astype(int)
    df['is_cultural_event'] = ((df['event_type_1'] == 'Cultural') | (df['event_type_2'] == 'Cultural')).astype(int)
    
    # Drop original event type columns as they're now encoded
    df = df.drop(['event_name_1', 'event_name_2', 'event_type_1', 'event_type_2'], axis=1)
    
    return df

def clean_sales_data(df):
    """Clean sales training dataset"""
    print("Cleaning sales data...")
    
    # Replace negative values with 0 (assuming negative sales are errors)
    sales_cols = [col for col in df.columns if col.startswith('d_')]
    df[sales_cols] = df[sales_cols].clip(lower=0)
    
    # Simple imputation for missing values in sales data
    # Strategy: Use median of same item's sales from other stores
    imputer = SimpleImputer(strategy='median')
    df[sales_cols] = imputer.fit_transform(df[sales_cols])
    
    return df

def clean_price_data(df):
    """Clean price dataset"""
    print("Cleaning price data...")
    
    # Handle missing prices
    # Strategy 1: Forward fill prices for each store-item combination
    df = df.sort_values(['store_id', 'item_id', 'wm_yr_wk'])
    df['sell_price'] = df.groupby(['store_id', 'item_id'])['sell_price'].fillna(method='ffill')
    
    # Strategy 2: For any remaining missing values, use median price of that item across stores
    df['sell_price'] = df.groupby('item_id')['sell_price'].transform(
        lambda x: x.fillna(x.median())
    )
    
    # Remove outliers using IQR method
    Q1 = df['sell_price'].quantile(0.25)
    Q3 = df['sell_price'].quantile(0.75)
    IQR = Q3 - Q1
    df['sell_price'] = df['sell_price'].clip(
        lower=Q1 - 1.5*IQR,
        upper=Q3 + 1.5*IQR
    )
    
    return df

def main():
    # Clean each dataset
    calendar_clean = clean_calendar_data(calendar_df)
    sales_clean = clean_sales_data(sales_train_validation_df)
    prices_clean = clean_price_data(sell_prices_df)
    
    # Save cleaned datasets
    calendar_clean.to_csv('m5-forecasting-accuracy/calendar_clean.csv', index=False)
    sales_clean.to_csv('m5-forecasting-accuracy/sales_train_validation_clean.csv', index=False)
    prices_clean.to_csv('m5-forecasting-accuracy/sell_prices_clean.csv', index=False)
    
    # Print summary of cleaning
    print("\nCleaning Summary:")
    print(f"Calendar data shape: {calendar_clean.shape}")
    print(f"Sales data shape: {sales_clean.shape}")
    print(f"Price data shape: {prices_clean.shape}")
    
    # Print missing values summary
    print("\nMissing values after cleaning:")
    print("\nCalendar:")
    print(calendar_clean.isnull().sum())
    print("\nSales:")
    print(sales_clean.isnull().sum().sum())
    print("\nPrices:")
    print(prices_clean.isnull().sum())

if __name__ == "__main__":
    main()
