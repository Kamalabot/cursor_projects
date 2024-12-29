import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error, mean_absolute_error
from xgboost import XGBRegressor
from baseline_sma import create_sma_predictions
from evaluation_metric import WRMSSEEvaluator, calculate_wrmsse

def create_baseline_model(sales_df, calendar_df):
    """
    Creates a baseline time series model using XGBoost
    
    Parameters:
    -----------
    sales_df : DataFrame
        Contains the sales data with columns: ['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id'] 
        and d_1 through d_1969 for daily sales
    calendar_df : DataFrame
        Contains the calendar information
    
    Returns:
    --------
    model : XGBRegressor
        Trained model
    feature_cols : list
        List of feature columns used
    """
    
    # Prepare calendar features
    calendar_features = calendar_df.copy()
    
    # Create day of week dummies
    dow_dummies = pd.get_dummies(calendar_features['wday'], prefix='dow')
    calendar_features = pd.concat([calendar_features, dow_dummies], axis=1)
    
    # Create month dummies
    month_dummies = pd.get_dummies(calendar_features['month'], prefix='month')
    calendar_features = pd.concat([calendar_features, month_dummies], axis=1)
    
    # Create event type features
    calendar_features['is_holiday'] = calendar_features['event_type_1'].notna().astype(int)
    calendar_features['is_religious'] = (calendar_features['event_type_1'] == 'Religious').astype(int)
    calendar_features['is_national'] = (calendar_features['event_type_1'] == 'National').astype(int)
    calendar_features['is_cultural'] = (calendar_features['event_type_1'] == 'Cultural').astype(int)
    calendar_features['is_sporting'] = (calendar_features['event_type_1'] == 'Sporting').astype(int)
    
    # Create lag features
    def create_lag_features(data, lags=[7, 14, 28]):
        lag_cols = []
        for lag in lags:
            col_name = f'sales_lag_{lag}'
            data[col_name] = data['sales'].shift(lag)
            lag_cols.append(col_name)
        return data, lag_cols

    # Melt sales data to long format
    sales_long = pd.melt(
        sales_df,
        id_vars=['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id'],
        var_name='d',
        value_name='sales'
    )
    
    # Merge with calendar features
    sales_long = sales_long.merge(calendar_features, on='d', how='left')
    
    # Create lag features
    sales_long = sales_long.sort_values(['id', 'date'])
    sales_long, lag_cols = create_lag_features(sales_long)
    
    # Define feature columns
    feature_cols = (
        list(dow_dummies.columns) +
        list(month_dummies.columns) +
        ['is_holiday', 'is_religious', 'is_national', 'is_cultural', 'is_sporting'] +
        lag_cols
    )
    
    # Remove rows with NaN values (due to lag features)
    sales_long = sales_long.dropna()
    
    # Train model
    model = XGBRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )
    
    X = sales_long[feature_cols]
    y = sales_long['sales']
    
    model.fit(X, y)
    
    return model, feature_cols

def make_predictions(model, feature_cols, new_data):
    """
    Make predictions using the trained model
    
    Parameters:
    -----------
    model : XGBRegressor
        Trained model
    feature_cols : list
        List of feature columns used by the model
    new_data : DataFrame
        New data to make predictions on
        
    Returns:
    --------
    predictions : array
        Array of predicted sales
    """
    return model.predict(new_data[feature_cols])

def compare_with_sma(xgb_predictions, sma_results, first_5_products, evaluator):
    """Compare XGBoost predictions with SMA predictions using WRMSSE"""
    comparison = pd.DataFrame({
        'model': ['XGBoost'] + [f'SMA-{window}' for window in sma_results.keys()],
        'wrmsse': [
            evaluator.score(xgb_predictions)
        ] + [
            evaluator.score(data['predictions']) for data in sma_results.values()
        ],
        'rmse': [
            mean_squared_error(sma_results[7]['actuals'], xgb_predictions, squared=False)
        ] + [
            data['rmse'] for data in sma_results.values()
        ]
    })
    
    return comparison

# Example usage:
# Load your data
sales_df = pd.read_csv('sales_data.csv')
calendar_df = pd.read_csv('calendar.csv')

# Create and train the model
model, feature_cols = create_baseline_model(sales_df, calendar_df)

# Make predictions
predictions = make_predictions(model, feature_cols, new_data)

if __name__ == "__main__":
    # Load the data
    print("Loading data...")
    sales_df = pd.read_csv('m5-forecasting-accuracy/sales_train_validation.csv')
    calendar_df = pd.read_csv('m5-forecasting-accuracy/calendar.csv')
    
    # Select first 5 products
    print("Selecting first 5 products...")
    first_5_products = sales_df.head(5)
    print("\nSelected products:")
    print(first_5_products[['id', 'item_id', 'store_id', 'state_id']].to_string())
    
    # Create and train model
    print("\nTraining model...")
    model, feature_cols = create_baseline_model(first_5_products, calendar_df)
    
    # Prepare data for next 28 days prediction
    print("\nPreparing prediction data...")
    last_day = 'd_1969'  # Last day in the training data
    
    # Get the last 28 days of data for creating lag features
    history_data = first_5_products.melt(
        id_vars=['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id'],
        value_vars=[f'd_{i}' for i in range(1969-27, 1970)],
        var_name='d',
        value_name='sales'
    )
    
    # Get next 28 days from calendar
    future_dates = calendar_df[calendar_df['d'].isin([f'd_{i}' for i in range(1970, 1998)])]
    
    # Create prediction data
    prediction_data = pd.DataFrame()
    for _, product in first_5_products.iterrows():
        product_pred = future_dates.copy()
        for col in ['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id']:
            product_pred[col] = product[col]
        prediction_data = pd.concat([prediction_data, product_pred])
    
    # Create features for prediction data
    prediction_features = pd.get_dummies(prediction_data['wday'], prefix='dow')
    month_dummies = pd.get_dummies(prediction_data['month'], prefix='month')
    prediction_features = pd.concat([prediction_features, month_dummies], axis=1)
    
    # Add event features
    prediction_features['is_holiday'] = prediction_data['event_type_1'].notna().astype(int)
    prediction_features['is_religious'] = (prediction_data['event_type_1'] == 'Religious').astype(int)
    prediction_features['is_national'] = (prediction_data['event_type_1'] == 'National').astype(int)
    prediction_features['is_cultural'] = (prediction_data['event_type_1'] == 'Cultural').astype(int)
    prediction_features['is_sporting'] = (prediction_data['event_type_1'] == 'Sporting').astype(int)
    
    # Add lag features (using history data)
    for lag in [7, 14, 28]:
        col_name = f'sales_lag_{lag}'
        prediction_features[col_name] = np.nan  # Will be filled with actual values
    
    # Make predictions
    print("\nMaking predictions...")
    predictions = make_predictions(model, feature_cols, prediction_features)
    
    # Create results DataFrame
    results = pd.DataFrame({
        'id': prediction_data['id'],
        'date': prediction_data['date'],
        'predicted_sales': predictions
    })
    
    # Print results summary
    print("\nPrediction Results Summary:")
    print("===========================")
    for product_id in first_5_products['id']:
        product_predictions = results[results['id'] == product_id]
        print(f"\nProduct ID: {product_id}")
        print(f"Average predicted daily sales: {product_predictions['predicted_sales'].mean():.2f}")
        print(f"Min predicted sales: {product_predictions['predicted_sales'].min():.2f}")
        print(f"Max predicted sales: {product_predictions['predicted_sales'].max():.2f}")
    
    # Save predictions to CSV
    results.to_csv('first_5_products_predictions.csv', index=False)
    print("\nPredictions saved to 'first_5_products_predictions.csv'")
    
    # Optional: Plot predictions
    try:
        import plotly.express as px
        
        fig = px.line(results, x='date', y='predicted_sales', color='id',
                     title='Predicted Sales for First 5 Products')
        fig.write_html('predictions_plot.html')
        print("Predictions plot saved as 'predictions_plot.html'")
    except ImportError:
        print("Plotly not installed. Skipping visualization.")
    
    # After making XGBoost predictions, add:
    print("\nCalculating SMA predictions for comparison...")
    sma_results = create_sma_predictions(first_5_products, calendar_df)
    
    # Compare results
    comparison = compare_with_sma(predictions, sma_results, first_5_products, evaluator)
    
    print("\nModel Comparison:")
    print("================")
    print(comparison.to_string(index=False))
    
    # Save comparison
    comparison.to_csv('model_comparison.csv', index=False)
    print("\nComparison saved to 'model_comparison.csv'")
    
    # Create comparison plot
    try:
        fig = px.bar(comparison, x='model', y=['rmse', 'wrmsse'],
                     title='Model Comparison: XGBoost vs SMA',
                     barmode='group')
        fig.write_html('model_comparison.html')
        print("Comparison plot saved as 'model_comparison.html'")
    except ImportError:
        print("Plotly not installed. Skipping visualization.")