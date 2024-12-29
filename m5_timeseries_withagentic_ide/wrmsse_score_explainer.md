

The Weighted Root Mean Squared Scaled Error (WRMSSE) is a more sophisticated evaluation metric that accounts for both the scale of the data and the relative importance of different items. Here's the theory and implementation:

```python:evaluation_metric.py
import numpy as np
import pandas as pd

class WRMSSEEvaluator:
    """
    Weighted Root Mean Squared Scaled Error Evaluator
    
    This evaluator is specific to the M5 competition which considers both:
    1. Scale of each time series (using scaling factor)
    2. Weight of each series (based on dollar sales)
    """
    
    def __init__(self, train_df, valid_df, calendar_df, prices_df):
        """
        Initialize the WRMSSEEvaluator
        
        Parameters:
        -----------
        train_df : pd.DataFrame
            Training data with actual sales
        valid_df : pd.DataFrame
            Validation data with actual sales
        calendar_df : pd.DataFrame
            Calendar information
        prices_df : pd.DataFrame
            Price information
        """
        self.calendar = calendar_df
        self.prices = prices_df
        self.train = train_df
        self.valid = valid_df
        
        self.train_df = train_df.copy()
        self.valid_df = valid_df.copy()
        self.calendar_df = calendar_df.copy()
        self.prices_df = prices_df.copy()
        
        self.weight_df = None
        self.scale_df = None
        self.train_series = None
        self.valid_series = None
        
        self._prepare_data()
    
    def _prepare_data(self):
        """Prepare data for WRMSSE calculation"""
        # Calculate dollar sales for weights
        self.train_series, self.valid_series = self._get_series()
        self.weight_df = self._get_weights()
        self.scale_df = self._get_scale()
        
    def _get_series(self):
        """Convert training and validation data into series"""
        # Get product information
        product_info = self.train_df[['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id']]
        
        # Melt training data
        train_series = pd.melt(self.train_df, 
                              id_vars=['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id'],
                              var_name='d',
                              value_name='value')
        
        # Melt validation data
        valid_series = pd.melt(self.valid_df,
                              id_vars=['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id'],
                              var_name='d',
                              value_name='value')
        
        return train_series, valid_series
    
    def _get_weights(self):
        """Calculate weights based on dollar sales"""
        # Merge sales data with prices
        sales_price = self.train_series.merge(self.prices_df, 
                                            on=['store_id', 'item_id'],
                                            how='left')
        
        # Calculate dollar sales
        sales_price['dollar_sales'] = sales_price['value'] * sales_price['sell_price']
        
        # Calculate weights at different levels
        weights = sales_price.groupby(['id'])['dollar_sales'].sum()
        weights = weights / weights.sum()
        
        return weights
    
    def _get_scale(self):
        """Calculate scaling factors"""
        # Calculate scale as mean squared error of naive forecast
        train_series = self.train_series.copy()
        train_series['value_lag'] = train_series.groupby(['id'])['value'].shift(28)
        train_series = train_series.dropna()
        
        scale = train_series.groupby(['id']).apply(
            lambda x: np.sqrt(np.mean((x['value'] - x['value_lag'])**2))
        )
        
        return scale
    
    def score(self, predictions):
        """
        Calculate WRMSSE score
        
        Parameters:
        -----------
        predictions : np.array
            Predicted values
            
        Returns:
        --------
        float
            WRMSSE score
        """
        # Reshape predictions if necessary
        if isinstance(predictions, pd.DataFrame):
            predictions = predictions.values
            
        # Calculate scaled errors
        errors = (self.valid_series['value'].values - predictions)
        scaled_errors = errors / self.scale_df.values.reshape(-1, 1)
        
        # Calculate RMSSE for each series
        rmsse = np.sqrt(np.mean(scaled_errors**2, axis=1))
        
        # Calculate weighted average
        wrmsse = np.sum(rmsse * self.weight_df.values)
        
        return wrmsse

def calculate_wrmsse(y_true, y_pred, scale, weights):
    """
    Simplified WRMSSE calculation for single-level comparison
    
    Parameters:
    -----------
    y_true : array-like
        Actual values
    y_pred : array-like
        Predicted values
    scale : array-like
        Scaling factors for each series
    weights : array-like
        Weights for each series
        
    Returns:
    --------
    float
        WRMSSE score
    """
    # Calculate scaled errors
    errors = np.array(y_true) - np.array(y_pred)
    scaled_errors = errors / scale.reshape(-1, 1)
    
    # Calculate RMSSE for each series
    rmsse = np.sqrt(np.mean(scaled_errors**2, axis=1))
    
    # Calculate weighted average
    wrmsse = np.sum(rmsse * weights)
    
    return wrmsse
```

The theory behind WRMSSE:

1. **Scaling Factor**:
   - Each time series is scaled by its own "typical" prediction error
   - The scaling factor is calculated using a naive forecast (28-day lag)
   - This makes errors comparable across different scales of data

2. **Weights**:
   - Each series is weighted by its relative importance
   - In M5, weights are based on dollar sales
   - Higher-selling items have more impact on the final score

3. **Formula**:
   ```
   WRMSSE = Σ(w_i * RMSSE_i)
   
   where:
   RMSSE_i = sqrt(mean((y_true - y_pred)^2)) / scale_i
   w_i = dollar_sales_i / total_dollar_sales
   scale_i = sqrt(mean((y_t - y_{t-28})^2))
   ```

To use this in your existing models:

```python:baseline_xgbmodel.py
# Add to imports
from evaluation_metric import WRMSSEEvaluator, calculate_wrmsse

# Update the comparison function
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
```

This metric better reflects the competition's goals by:
1. Accounting for different scales of items
2. Giving more weight to important items
3. Making errors comparable across different series

The lower the WRMSSE score, the better the model's performance.
