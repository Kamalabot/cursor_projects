import pandas as pd
import os

# Load the data files
calendar_df = pd.read_csv('m5-forecasting-accuracy/calendar.csv')
sales_train_validation_df = pd.read_csv('m5-forecasting-accuracy/sales_train_validation.csv')
sample_submission_df = pd.read_csv('m5-forecasting-accuracy/sample_submission.csv')
sell_prices_df = pd.read_csv('m5-forecasting-accuracy/sell_prices.csv')
sales_train_evaluation_df = pd.read_csv('m5-forecasting-accuracy/sales_train_evaluation.csv')

# Function to display basic information about each dataframe
def examine_dataframe(df, name):
    print(f"\n=== {name} ===")
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nColumns:", df.columns.tolist())
    print("\nShape:", df.shape)
    print("\n" + "="*50)

# Examine each dataframe
examine_dataframe(calendar_df, "Calendar Data")
examine_dataframe(sales_train_validation_df, "Sales Train Validation Data")
examine_dataframe(sample_submission_df, "Sample Submission Data")
examine_dataframe(sell_prices_df, "Sell Prices Data")
examine_dataframe(sales_train_evaluation_df, "Sales Train Evaluation Data")
