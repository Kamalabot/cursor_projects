import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def load_data():
    """Load the cleaned calendar data"""
    calendar = pd.read_csv('m5-forecasting-accuracy/calendar_clean.csv')
    calendar['date'] = pd.to_datetime(calendar['date'])
    calendar['year'] = calendar['date'].dt.year
    calendar['month'] = calendar['date'].dt.month
    return calendar

def create_event_distribution(calendar):
    """Create a bar chart showing distribution of events by month"""
    # Create event flag using the 'events' column from cleaned data
    calendar['has_event'] = calendar['events'].notna()
    
    # Group by month and count events
    monthly_events = calendar.groupby(['year', 'month'])['has_event'].sum().reset_index()
    
    # Convert year and month to integers before formatting
    monthly_events['year'] = monthly_events['year'].astype(int)
    monthly_events['month'] = monthly_events['month'].astype(int)
    
    # Create month-year string for better display
    monthly_events['month_year'] = monthly_events.apply(
        lambda x: f"{int(x['year'])}-{int(x['month']):02d}", axis=1
    )
    
    fig = px.bar(monthly_events, 
                 x='month_year', 
                 y='has_event',
                 title='Number of Events by Month',
                 labels={'has_event': 'Number of Events', 'month_year': 'Month-Year'})
    
    fig.update_xaxes(tickangle=45)
    return fig

def create_holiday_type_distribution(calendar):
    """Create a pie chart showing distribution of holiday types"""
    holiday_counts = calendar[['is_national_holiday', 'is_religious_holiday', 'is_cultural_event']].sum()
    
    fig = px.pie(values=holiday_counts.values, 
                 names=['National Holidays', 'Religious Holidays', 'Cultural Events'],
                 title='Distribution of Holiday Types')
    return fig

def create_snap_analysis(calendar):
    """Create analysis of SNAP patterns"""
    # Calculate SNAP statistics by month
    snap_monthly = calendar.groupby(['year', 'month'])[['snap_CA', 'snap_TX', 'snap_WI']].mean()
    snap_monthly = snap_monthly.reset_index()
    
    # Convert year and month to integers before formatting
    snap_monthly['year'] = snap_monthly['year'].astype(int)
    snap_monthly['month'] = snap_monthly['month'].astype(int)
    
    snap_monthly['month_year'] = snap_monthly.apply(
        lambda x: f"{int(x['year'])}-{int(x['month']):02d}", axis=1
    )
    
    fig = px.line(snap_monthly, 
                  x='month_year',
                  y=['snap_CA', 'snap_TX', 'snap_WI'],
                  title='SNAP Program Patterns by State',
                  labels={'value': 'SNAP Proportion', 'month_year': 'Month-Year'})
    
    fig.update_xaxes(tickangle=45)
    return fig

def create_weekday_event_pattern(calendar):
    """Create analysis of events by day of week"""
    calendar['has_event'] = calendar['events'].notna()
    weekday_events = calendar[calendar['has_event']]['wday'].value_counts().sort_index()
    
    # Map numeric days to names
    day_names = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 
                 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
    weekday_events.index = weekday_events.index.map(day_names)
    
    fig = px.bar(x=weekday_events.index, 
                 y=weekday_events.values,
                 title='Distribution of Events by Day of Week',
                 labels={'x': 'Day of Week', 'y': 'Number of Events'})
    return fig

def main():
    """Main function to create and save all visualizations"""
    calendar = load_data()
    
    # Create all plots
    event_dist = create_event_distribution(calendar)
    holiday_types = create_holiday_type_distribution(calendar)
    snap_analysis = create_snap_analysis(calendar)
    weekday_pattern = create_weekday_event_pattern(calendar)
    
    # Create a subplot figure to combine all visualizations
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Events by Month', 'Holiday Types Distribution',
                       'SNAP Patterns by State', 'Events by Day of Week'),
        specs=[[{'type': 'xy'}, {'type': 'domain'}],
               [{'type': 'xy'}, {'type': 'xy'}]]
    )
    
    # Add traces from individual plots to subplots
    for trace in event_dist.data:
        fig.add_trace(trace, row=1, col=1)
    
    for trace in holiday_types.data:
        fig.add_trace(trace, row=1, col=2)
    
    for trace in snap_analysis.data:
        fig.add_trace(trace, row=2, col=1)
    
    for trace in weekday_pattern.data:
        fig.add_trace(trace, row=2, col=2)
    
    # Update layout
    fig.update_layout(height=1000, width=1200, title_text="Calendar Data Analysis")
    
    # Save plots
    fig.write_html("calendar_analysis.html")
    
    # Also save individual plots
    event_dist.write_html("event_distribution.html")
    holiday_types.write_html("holiday_types.html")
    snap_analysis.write_html("snap_analysis.html")
    weekday_pattern.write_html("weekday_pattern.html")

if __name__ == "__main__":
    main() 