import pandas as pd

def clean_project_data(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)
    
    # Initialize lists to store transformed data
    projects = []
    quarters = []
    plan_values = []
    actual_values = []
    
    # Iterate through the dataframe rows
    for i in range(0, len(df), 2):  # Step by 2 since each project has 2 rows
        project = df.iloc[i]['Project']
        quarter = df.iloc[i]['Quarter']
        plan_revenue = df.iloc[i]['Revenue']
        actual_revenue = df.iloc[i+1]['Revenue']
        
        # Append values to lists
        projects.append(project)
        quarters.append(quarter)
        plan_values.append(plan_revenue)
        actual_values.append(actual_revenue)
    
    # Create cleaned dataframe
    cleaned_df = pd.DataFrame({
        'Project': projects,
        'Quarter': quarters,
        'Planned_Revenue': plan_values,
        'Actual_Revenue': actual_values
    })
    
    # Add additional calculated columns
    cleaned_df['Variance'] = cleaned_df['Actual_Revenue'] - cleaned_df['Planned_Revenue']
    cleaned_df['Variance_Percentage'] = (cleaned_df['Variance'] / cleaned_df['Planned_Revenue'] * 100).round(2)
    
    # Extract quarter number from Quarter column (Q1 -> 1)
    cleaned_df['Quarter_Num'] = cleaned_df['Quarter'].str.extract('(\d+)').astype(int)
    
    # Sort the dataframe
    cleaned_df = cleaned_df.sort_values(['Quarter_Num', 'Project'])
    
    # Save the cleaned data
    # cleaned_df.to_excel('cleaned_project_data.xlsx', index=False)
    
    return cleaned_df


# Usage
if __name__ == "__main__":
    file_path = "project_data.xlsx"
    cleaned_data = clean_project_data(file_path)
    print(cleaned_data.head(2))
    print(cleaned_data.columns)
    print("Data cleaning completed successfully!")
