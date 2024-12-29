import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
import plotly.express as px

def create_sma_predictions(sales_df, calendar_df, window_sizes=[7, 14, 28], n_forecast_days=28):
    """
    Creates predictions using Simple Moving Average with different window sizes
    
    Parameters:
    -----------
    sales_df : DataFrame
        Sales data
    calendar_df : DataFrame
        Calendar data
    window_sizes : list
        List of window sizes for moving averages
    n_forecast_days : int
        Number of days to forecast
        
    Returns:
    --------
    dict : Dictionary containing predictions and metrics for each window size
    """
    
    # Melt sales data to long format
    sales_long = pd.melt(
        sales_df,
        id_vars=['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id'],
        var_name='d',
        value_name='sales'
    )
    
    # Merge with calendar
    sales_long = sales_long.merge(calendar_df[['d', 'date']], on='d', how='left')
    sales_long['date'] = pd.to_datetime(sales_long['date'])
    
    results = {}
    
    for window in window_sizes:
        print(f"\nCalculating {window}-day moving average...")
        
        # Calculate moving average for each product
        predictions = []
        actuals = []
        
        for name, group in sales_long.groupby('id'):
            # Sort by date
            group = group.sort_values('date')
            
            # Calculate moving average
            ma = group['sales'].rolling(window=window, min_periods=1).mean()
            
            # Get last window days for prediction
            last_ma = ma.iloc[-1]
            
            # Create prediction array
            pred = np.array([last_ma] * n_forecast_days)
            predictions.append(pred)
            
            # Store last 28 days of actual values for comparison
            actuals.append(group['sales'].iloc[-n_forecast_days:].values)
        
        predictions = np.vstack(predictions)
        actuals = np.vstack(actuals)
        
        # Calculate metrics
        mse = mean_squared_error(actuals, predictions)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(actuals, predictions)
        
        results[window] = {
            'predictions': predictions,
            'actuals': actuals,
            'mse': mse,
            'rmse': rmse,
            'mae': mae
        }
        
        print(f"Window {window} - RMSE: {rmse:.2f}, MAE: {mae:.2f}")
    
    return results

def plot_sma_predictions(results, product_idx=0):
    """
    Plot predictions for a single product using different window sizes
    """
    fig = px.line(title=f'SMA Predictions for Product {product_idx}')
    
    # Plot actual values
    actuals = results[list(results.keys())[0]]['actuals'][product_idx]
    fig.add_scatter(y=actuals, name='Actual', mode='lines')
    
    # Plot predictions for each window size
    for window, data in results.items():
        predictions = data['predictions'][product_idx]
        fig.add_scatter(y=predictions, name=f'SMA-{window}', mode='lines')
    
    return fig

if __name__ == "__main__":
    # Load data
    print("Loading data...")
    sales_df = pd.read_csv('m5-forecasting-accuracy/sales_train_validation.csv')
    calendar_df = pd.read_csv('m5-forecasting-accuracy/calendar.csv')
    
    # Select first 5 products
    print("Selecting first 5 products...")
    first_5_products = sales_df.head(5)
    
    # Create SMA predictions
    sma_results = create_sma_predictions(first_5_products, calendar_df)
    
    # Save results
    results_df = pd.DataFrame({
        'window_size': list(sma_results.keys()),
        'rmse': [data['rmse'] for data in sma_results.values()],
        'mae': [data['mae'] for data in sma_results.values()]
    })
    results_df.to_csv('sma_results.csv', index=False)
    print("\nResults saved to 'sma_results.csv'")
    
    # Create and save plots
    for i in range(5):
        fig = plot_sma_predictions(sma_results, i)
        fig.write_html(f'sma_predictions_product_{i}.html')
    print("Prediction plots saved as HTML files") 