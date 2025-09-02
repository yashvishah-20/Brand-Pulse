import pandas as pd
import plotly.graph_objects as go

file_path = r"C:\Users\PraveenChaudhary\Desktop\data\LRCX_twitter_sentiment.xlsx"
df = pd.read_excel(file_path,sheet_name="Sheet1")
# order the columns Date in increasing order
df = df.sort_values(by='date type')

# Fix column formatting
df.columns = df.columns.str.strip()


# Use 'date type' as the date column
if 'date type' not in df.columns:
    raise ValueError(f"Expected column 'date type', found: {df.columns.tolist()}")

# Parse Date
df['date type'] = pd.to_datetime(df['date type'])

# Preprocess MonthYear
df['MonthYear'] = df['date type'].dt.strftime('%B %Y')

# Data for MonthYear view (line chart)
monthyear_data = df.groupby(['MonthYear', 'Sentiment']).size().reset_index(name='Count')

# Convert MonthYear to datetime for sorting and filtering
monthyear_data['MonthYear_dt'] = pd.to_datetime(monthyear_data['MonthYear'], format='%B %Y')
monthyear_data = monthyear_data.sort_values(by='MonthYear_dt')
monthyear_data['MonthYear_str'] = monthyear_data['MonthYear_dt'].dt.strftime('%b %Y')

# Get available years for filter
all_years = monthyear_data['MonthYear_dt'].dt.year.unique()
min_year = int(monthyear_data['MonthYear_dt'].dt.year.min())
max_year = int(monthyear_data['MonthYear_dt'].dt.year.max())

# User can set these values as needed
start_year = min_year  # Change as needed
end_year = max_year    # Change as needed

# Filter data by year range
mask = (monthyear_data['MonthYear_dt'].dt.year >= start_year) & (monthyear_data['MonthYear_dt'].dt.year <= end_year)
filtered_monthyear_data = monthyear_data[mask]

# Initialize figure
fig = go.Figure()

# Add Line traces for Month-Year
for sentiment in ['Positive', 'Neutral', 'Negative']:
    filtered = filtered_monthyear_data[filtered_monthyear_data['Sentiment'] == sentiment]
    fig.add_trace(go.Scatter(
        x=filtered['MonthYear_dt'],
        y=filtered['Count'],
        name=sentiment,
        mode='lines+markers',
        visible=True,
        marker=dict(size=8),
        line=dict(width=2),
        marker_color={"Positive": "green", "Neutral": "gray", "Negative": "red"}[sentiment]
    ))

# Add a year range slider for interactive filtering
fig.update_layout(
    xaxis=dict(
        title="Month-Year",
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="<span style='color:#1f77b4'><b>1y</b></span>", step="year", stepmode="backward"),
                dict(count=2, label="<span style='color:#ff7f0e'><b>2y</b></span>", step="year", stepmode="backward"),
                dict(label="<span style='color:#2ca02c'><b>All</b></span>", step="all")
            ]),
            font=dict(color="#fff"),
            activecolor="#222"
        ),
        rangeslider=dict(
            visible=True,
            thickness=0.08
        ),
        type="date"
    )
)

# Final layout
fig.update_layout(
    title="Twitter Sentiment Distribution (Monthly Line Chart)",
    template="plotly_dark",
    yaxis_title="Number of Posts",
    legend_title="Sentiment",
    height=600,
    width=1000
)

fig.show()
