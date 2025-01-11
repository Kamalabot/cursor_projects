import pandas as pd
import numpy as np

# Create sample data
projects = ['Project A', 'Project B', 'Project C', 'Project D', 'Project E',
            'Project F', 'Project G', 'Project H', 'Project I', 'Project J']
quarters = ['Q1', 'Q1', 'Q2', 'Q2', 'Q3', 'Q3', 'Q4', 'Q4', 'Q4', 'Q4']
revenues_plan = [100000, 150000, 200000, 180000, 250000, 300000, 280000, 320000, 270000, 350000]
revenues_actual = [98000, 155000, 205000, 175000, 260000, 290000, 285000, 325000, 268000, 360000]

# Create the main data rows
main_data = pd.DataFrame({
    'Project': projects,
    'Quarter': quarters,
    '': '',  # Empty column for alignment
    'Revenue': ''  # Empty column for alignment
})

# Create the plan/actual rows
plan_actual_data = []
for plan, actual in zip(revenues_plan, revenues_actual):
    plan_actual_data.extend([
        ['', '', 'Plan', plan],
        ['', '', 'Actual', actual]
    ])

plan_actual_df = pd.DataFrame(plan_actual_data, columns=main_data.columns)

# Combine the dataframes
final_df = pd.concat([main_data, plan_actual_df])

# Save to Excel file
with pd.ExcelWriter('project_data.xlsx', engine='openpyxl') as writer:
    final_df.to_excel(writer, sheet_name='Projects', index=False)