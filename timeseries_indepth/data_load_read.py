import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load the main datasets
train_df = pd.read_csv('store-sales-time-series-forecasting/train.csv')
test_df = pd.read_csv('store-sales-time-series-forecasting/test.csv')
stores_df = pd.read_csv('store-sales-time-series-forecasting/stores.csv')
transactions_df = pd.read_csv('store-sales-time-series-forecasting/transactions.csv')
oil_df = pd.read_csv('store-sales-time-series-forecasting/oil.csv')
holidays_df = pd.read_csv('store-sales-time-series-forecasting/holidays_events.csv')

# Initial data exploration
print("\nTrain Dataset Shape:", train_df.shape)
print("\nFirst few rows of training data:")
print(train_df.head())
print("\nData Info:")
print(train_df.info())

# Convert date columns to datetime
def prepare_data(df):
    df['date'] = pd.to_datetime(df['date'])
    
    # Merge with store information
    df = df.merge(stores_df, on='store_nbr', how='left')
    
    # Extract time-based features
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_of_week'] = df['date'].dt.dayofweek
    
    return df

# Prepare training data
train_df = prepare_data(train_df)

# Basic statistics
# print("\nBasic statistics of sales:")
# print(train_df['sales'].describe())

# Create time series visualization
def plot_sales_trends():
    plt.figure(figsize=(15, 6))
    
    # Daily sales
    daily_sales = train_df.groupby('date')['sales'].sum().reset_index()
    plt.plot(daily_sales['date'], daily_sales['sales'])
    
    plt.title('Daily Total Sales Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Sales')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Monthly sales pattern
    plt.figure(figsize=(12, 6))
    monthly_sales = train_df.groupby(['year', 'month'])['sales'].sum().reset_index()
    sns.boxplot(data=train_df, x='month', y='sales')
    plt.title('Monthly Sales Distribution')
    plt.show()

# plot_sales_trends()

# Store-wise analysis
def analyze_stores():
    store_sales = train_df.groupby('store_nbr')['sales'].agg(['mean', 'std', 'count']).reset_index()
    store_sales = store_sales.merge(stores_df, on='store_nbr', how='left')
    
    plt.figure(figsize=(12, 6))
    sns.barplot(data=store_sales, x='city', y='mean')
    plt.title('Average Sales by City')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

analyze_stores()