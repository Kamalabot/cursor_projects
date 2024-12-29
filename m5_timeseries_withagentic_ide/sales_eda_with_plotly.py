import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Read the data
sell_prices = pd.read_csv('m5-forecasting-accuracy/sell_prices_clean.csv')

# Create figure for price analysis
fig1 = make_subplots(rows=2, cols=2,
                     subplot_titles=('Price Distribution by Store', 
                                   'Average Price Trends Over Time',
                                   'Price Range by Store',
                                   'Price Volatility by Store'))

# 1. Price Distribution by Store
store_price_dist = sell_prices.groupby('store_id')['sell_price'].mean()

fig1.add_trace(
    go.Bar(x=store_price_dist.index, y=store_price_dist.values, 
           name='Average Price'),
    row=1, col=1
)

# 2. Average Price Trends Over Time
price_trends = sell_prices.groupby('wm_yr_wk')['sell_price'].mean()

fig1.add_trace(
    go.Scatter(x=price_trends.index, y=price_trends.values, 
               mode='lines+markers', name='Price Trend'),
    row=1, col=2
)

# 3. Price Range by Store
price_range = sell_prices.groupby('store_id').agg({
    'sell_price': ['min', 'max', 'mean']
})['sell_price']

fig1.add_trace(
    go.Box(x=sell_prices['store_id'], y=sell_prices['sell_price'], 
           name='Price Range'),
    row=2, col=1
)

# 4. Price Volatility (Standard Deviation) by Store
price_volatility = sell_prices.groupby('store_id')['sell_price'].std()

fig1.add_trace(
    go.Bar(x=price_volatility.index, y=price_volatility.values, 
           name='Price Volatility'),
    row=2, col=2
)

# Update layout
fig1.update_layout(height=800, width=1200, title_text="Price Analysis by Store")
fig1.write_html("price_analysis_by_store.html")

# Create second figure for item analysis
fig2 = make_subplots(rows=2, cols=2,
                     subplot_titles=('Top 10 Most Expensive Items',
                                   'Price Distribution by Item (Sample)',
                                   'Items with Highest Price Variance',
                                   'Price Changes Frequency by Item'))

# 1. Top 10 Most Expensive Items
top_items = sell_prices.groupby('item_id')['sell_price'].mean().nlargest(10)

fig2.add_trace(
    go.Bar(x=top_items.index, y=top_items.values, 
           name='Average Price'),
    row=1, col=1
)

# 2. Price Distribution for Sample Items (top 5 items)
sample_items = top_items.head().index
sample_prices = sell_prices[sell_prices['item_id'].isin(sample_items)]

fig2.add_trace(
    go.Box(x=sample_prices['item_id'], y=sample_prices['sell_price'], 
           name='Price Distribution'),
    row=1, col=2
)

# 3. Items with Highest Price Variance
price_variance = sell_prices.groupby('item_id')['sell_price'].std().nlargest(10)

fig2.add_trace(
    go.Bar(x=price_variance.index, y=price_variance.values, 
           name='Price Variance'),
    row=2, col=1
)

# 4. Price Changes Frequency
price_changes = sell_prices.groupby(['item_id', 'wm_yr_wk'])['sell_price'].nunique()
frequent_changes = price_changes.groupby('item_id').sum().nlargest(10)

fig2.add_trace(
    go.Bar(x=frequent_changes.index, y=frequent_changes.values, 
           name='Price Changes'),
    row=2, col=2
)

# Update layout
fig2.update_layout(height=800, width=1200, title_text="Price Analysis by Item")
fig2.write_html("price_analysis_by_item.html")

# Additional statistics
print("\nBasic Statistics:")
print("=================")
print(f"Total number of unique items: {sell_prices['item_id'].nunique()}")
print(f"Total number of unique stores: {sell_prices['store_id'].nunique()}")
print(f"Average price across all items: ${sell_prices['sell_price'].mean():.2f}")
print(f"Median price across all items: ${sell_prices['sell_price'].median():.2f}")
print(f"Price range: ${sell_prices['sell_price'].min():.2f} - ${sell_prices['sell_price'].max():.2f}") 