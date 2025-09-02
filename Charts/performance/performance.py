# Performance Donut Charts for All Platforms
import pandas as pd
import plotly.graph_objects as go

# File paths for each platform
files = {
    'Market Beat': r"C:\Users\YashviShah\Downloads\LRCX_marketbeat_news.xlsx",
    'Reddit': r"C:\Users\YashviShah\Downloads\LRCX_reddit_sentiment.xlsx",
    'Stocktwits': r"C:\Users\YashviShah\Downloads\LRCX_stocktwits_sentiment.xlsx",
    'Twitter': r"C:\Users\YashviShah\Downloads\LRCX_twitter_sentiment.xlsx"
}

# Sheet name for all files
sheet_name = "Sheet1"

# Sentiment colors
sentiment_colors = {"Positive": "green", "Neutral": "gray", "Negative": "red"}

# Helper to get sentiment counts
def get_sentiment_counts(file, sheet, date_col=None):
    df = pd.read_excel(file, sheet_name=sheet)
    df.columns = df.columns.str.strip()
    # For Twitter, use 'date type' column
    if date_col and date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col])
    elif 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    # Count sentiments
    counts = df['Sentiment'].value_counts().reindex(['Positive', 'Neutral', 'Negative'], fill_value=0)
    return counts

# Prepare data for each platform
platform_data = {}
platform_date_col = {
    'Market Beat': 'Date',
    'Reddit': 'Date',
    'Stocktwits': 'Date',
    'Twitter': 'date type'
}
for platform, path in files.items():
    date_col = platform_date_col.get(platform)
    platform_data[platform] = get_sentiment_counts(path, sheet_name, date_col)

# Create subplots for donut charts
from plotly.subplots import make_subplots
fig = make_subplots(rows=1, cols=4, specs=[[{'type':'domain'}]*4], subplot_titles=list(platform_data.keys()))

for i, (platform, counts) in enumerate(platform_data.items(), 1):
    fig.add_trace(
        go.Pie(
            labels=counts.index,
            values=counts.values,
            name=platform,
            hole=0.5,
            marker_colors=[sentiment_colors.get(s, 'lightgray') for s in counts.index],
            textinfo='percent+label',
            showlegend=False
        ),
        row=1, col=i
    )

fig.update_layout(
    title_text="Sentiment Distribution Donut Charts by Platform",
    template="plotly_dark",
    height=500,
    width=1200
)

fig.show()
