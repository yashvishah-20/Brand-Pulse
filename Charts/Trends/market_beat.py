import pandas as pd
import plotly.graph_objects as go

# Load the Excel file
file_path = r"C:\Users\PraveenChaudhary\Desktop\data\LRCX_marketbeat_news.xlsx"
df = pd.read_excel(file_path, sheet_name="Sheet1")

# Preprocess
df['MonthYear'] = df['Month'].astype(str) + " " + df['Year'].astype(str)

# Data for MonthYear view (line chart)
monthyear_data = df.groupby(['MonthYear', 'Sentiment']).size().reset_index(name='Count')

# Data for Year view (bar chart)


# Sort MonthYear chronologically

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

# Add Bar traces for Year


# Dropdown buttons to toggle between views

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
    title="Market Beat Sentiment Distribution (Monthly Line Chart)",
    template="plotly_dark",
    yaxis_title="Number of News Articles",
    legend_title="Sentiment",
    height=600,
    width=1000
)

fig.show()
