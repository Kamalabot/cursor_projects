import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for consistent visualizations
plt.style.use('seaborn')
sns.set_palette("husl")

def load_and_validate_data(filepath):
    """Load data with basic validation and type checking."""
    try:
        df = pd.read_csv(filepath)
        
        # Basic validation
        assert not df.empty, "Dataset is empty"
        assert df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) < 0.2, "Too many missing values"
        
        return df
    except Exception as e:
        raise ValueError(f"Data validation failed: {str(e)}")

def create_summary_stats(df):
    """Generate summary statistics using pandas methods."""
    return {
        'basic_stats': df.describe(),
        'missing_values': df.isnull().sum(),
        'data_types': df.dtypes
    }

def plot_distribution(df, column, title=None):
    """Create distribution plot with proper styling."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.histplot(data=df, x=column, kde=True, ax=ax)
    
    ax.set_title(title or f'Distribution of {column}')
    ax.set_xlabel(column)
    ax.set_ylabel('Count')
    
    plt.tight_layout()
    return fig 

def preprocess_data(df, categorical_columns=None, numerical_columns=None):
    """
    Preprocess dataframe with common cleaning operations.
    
    Args:
        df: pandas DataFrame
        categorical_columns: list of categorical column names
        numerical_columns: list of numerical column names
    """
    df_processed = df.copy()
    
    # Automatically identify column types if not specified
    if categorical_columns is None:
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns
    if numerical_columns is None:
        numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns
    
    # Handle missing values
    for col in numerical_columns:
        df_processed[col].fillna(df_processed[col].median(), inplace=True)
    for col in categorical_columns:
        df_processed[col].fillna(df_processed[col].mode()[0], inplace=True)
    
    # Convert categorical columns to category dtype
    for col in categorical_columns:
        df_processed[col] = df_processed[col].astype('category')
    
    return df_processed

def analyze_correlations(df, method='pearson', threshold=0.1):
    """
    Analyze and visualize correlations between numerical columns.
    
    Args:
        df: pandas DataFrame
        method: correlation method ('pearson', 'spearman', or 'kendall')
        threshold: minimum correlation coefficient to display
    """
    # Calculate correlation matrix
    corr_matrix = df.select_dtypes(include=['int64', 'float64']).corr(method=method)
    
    # Create correlation heatmap
    plt.figure(figsize=(12, 8))
    mask = np.abs(corr_matrix) < threshold
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', mask=mask, 
                center=0, vmin=-1, vmax=1)
    plt.title(f'Correlation Matrix ({method.capitalize()} method)')
    plt.tight_layout()
    
    return corr_matrix

def plot_boxplots(df, columns, figsize=(12, 6)):
    """
    Create boxplots for specified numerical columns.
    
    Args:
        df: pandas DataFrame
        columns: list of column names to plot
        figsize: tuple of figure dimensions
    """
    fig, ax = plt.subplots(figsize=figsize)
    df[columns].boxplot(ax=ax)
    plt.xticks(rotation=45)
    plt.title('Distribution of Numerical Variables')
    plt.tight_layout()
    return fig

def generate_summary_report(df):
    """
    Generate a comprehensive summary report of the dataset.
    """
    report = {
        'basic_info': {
            'rows': df.shape[0],
            'columns': df.shape[1],
            'duplicates': df.duplicated().sum(),
            'memory_usage': df.memory_usage().sum() / 1024**2  # in MB
        },
        'statistics': create_summary_stats(df),
        'column_types': {
            'numerical': df.select_dtypes(include=['int64', 'float64']).columns.tolist(),
            'categorical': df.select_dtypes(include=['object', 'category']).columns.tolist()
        }
    }
    return report