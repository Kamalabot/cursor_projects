import pandas as pd

def print_column_info():
    # Load all cleaned datasets
    calendar = pd.read_csv('m5-forecasting-accuracy/calendar_clean.csv')
    sales = pd.read_csv('m5-forecasting-accuracy/sales_train_validation_clean.csv')
    prices = pd.read_csv('m5-forecasting-accuracy/sell_prices_clean.csv')
    
    print("\n=== Calendar Columns ===")
    print(calendar.columns.tolist())
    
    print("\n=== Sales Columns ===")
    print(sales.columns.tolist())
    
    print("\n=== Prices Columns ===")
    print(prices.columns.tolist())

if __name__ == "__main__":
    print_column_info() 