import pandas as pd
from collections import Counter

# Path to your MarketBeat Excel file
file_path = r"C:\Users\PraveenChaudhary\Desktop\Brand\data\LRCX_stocktwits_sentiment.xlsx"

# Read the data from Sheet1
try:
    df = pd.read_excel(file_path, sheet_name="Sheet1")
except Exception as e:
    print(f"Error reading file: {e}")
    exit(1)

# Clean column names
if 'Sentiment' not in df.columns:
    df.columns = df.columns.str.strip()
    if 'Sentiment' not in df.columns:
        print(f"Sentiment column not found. Columns: {df.columns.tolist()}")
        print("First 5 rows:")
        print(df.head())
        exit(1)

# Count sentiment values
sentiment_counts = Counter(df['Sentiment'].dropna().str.strip())

# Print results for dashboard JS
print("MarketBeat Sentiment Counts:")
for sentiment in ['Positive', 'Neutral', 'Negative']:
    print(f"{sentiment}: {sentiment_counts.get(sentiment, 0)}")

# For direct JS array copy-paste
print("\nJS array for Chart.js:")
print([
    sentiment_counts.get('Positive', 0),
    sentiment_counts.get('Neutral', 0),
    sentiment_counts.get('Negative', 0)
])

# Write sentiment counts to JSON file for dashboard
import json
output_path = r"C:\Users\PraveenChaudhary\Desktop\Brand\lam_research_social_listening_dashboard\public\stocktwits_sentiment.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump({
        'Positive': sentiment_counts.get('Positive', 0),
        'Neutral': sentiment_counts.get('Neutral', 0),
        'Negative': sentiment_counts.get('Negative', 0)
    }, f)
print(f"Sentiment counts written to {output_path}")
