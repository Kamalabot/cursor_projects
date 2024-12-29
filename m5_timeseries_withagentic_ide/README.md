# M5 Forecasting - Accuracy Competition

This repository contains code for the [M5 Forecasting - Accuracy](https://www.kaggle.com/competitions/m5-forecasting-accuracy) Kaggle competition, which focuses on hierarchical sales forecasting.

## Competition Overview

The M5 competition uses hierarchical sales data from Walmart to predict future sales. Participants need to forecast daily sales for the next 28 days for over 30,000 products across 10 stores in 3 states.

### Key Details:
- **Objective**: Predict 28 days of daily sales data
- **Data**: Hierarchical sales information from Walmart stores
- **Evaluation**: Weighted Root Mean Squared Scaled Error (WRMSSE)
- **Timeline**: Competition ended April 30, 2020

## Getting Started

### Data Download
1. Visit the [competition page](https://www.kaggle.com/competitions/m5-forecasting-accuracy)
2. Accept the competition rules
3. Download the following files:
   - `calendar.csv` - Contains calendar information including holidays and events
   - `sales_train_validation.csv` - Daily unit sales data for 2011-2016
   - `sample_submission.csv` - Submission format example
   - `sell_prices.csv` - Weekly store-item prices
4. Place all downloaded files in the `m5-forecasting-accuracy` folder

### File Structure

m5-forecasting-accuracy/
├── calendar.csv
├── sales_train_validation.csv
├── sample_submission.csv
└── sell_prices.csv

### Data Description

1. **calendar.csv**
   - Contains date-related features and holiday/event information
   - Includes columns for weekday, month, year, and special events

2. **sales_train_validation.csv**
   - Daily unit sales data
   - Hierarchical structure (State/Store/Category/Department/Item)
   - Contains 1,941 days of historical data

3. **sell_prices.csv**
   - Weekly pricing data
   - Store-item level information

4. **sample_submission.csv**
   - Shows the required format for competition submissions

## Competition Metric

The evaluation metric is the Weighted Root Mean Squared Scaled Error (WRMSSE), which accounts for:
- Different aggregation levels in the hierarchy
- Scale differences between items
- Uncertainty in the forecasts

## License

Please refer to the [Kaggle competition rules](https://www.kaggle.com/competitions/m5-forecasting-accuracy/rules) for data usage terms and conditions.

