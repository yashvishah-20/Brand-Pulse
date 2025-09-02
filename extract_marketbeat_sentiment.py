import pandas as pd
import matplotlib.pyplot as plt
import json
from pathlib import Path

file_path = Path('data/LRCX_marketbeat_news.xlsx')
# Read only columns H, I, J (Sentiment, Month, Year) with header on the second row
# (header=1 means row 2 in Excel)
df = pd.read_excel(file_path, header=1, usecols="H:J")
print('Columns found in Excel file:', list(df.columns))

# Ensure required columns exist
if 'Month' not in df.columns or 'Year' not in df.columns or 'Sentiment' not in df.columns:
    raise ValueError("The file must contain 'Month', 'Year', and 'Sentiment' columns.")

# Filter for positive sentiment
df['is_positive'] = df['Sentiment'].str.lower().str.strip() == 'positive'

# Create a datetime column from Year and Month (use first day of month)
df['month_year'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str) + '-01')

# Group by month and year
monthly = df.groupby(df['month_year']).agg(
    total=('Sentiment', 'count'),
    positive=('is_positive', 'sum')
).reset_index()
monthly['positive_pct'] = (monthly['positive'] / monthly['total'] * 100).round(2)

# Prepare data for JSON
labels = monthly['month_year'].dt.strftime('%b %Y').tolist()
values = monthly['positive_pct'].tolist()
json_data = {
    'labels': labels,
    'positive': values
}

# Save JSON
json_path = Path('lam_research_social_listening_dashboard/public/lrcx_marketbeat_positive_trend.json')
json_path.parent.mkdir(parents=True, exist_ok=True)
with open(json_path, 'w') as f:
    json.dump(json_data, f, indent=2)

# Plot the line chart
plt.figure(figsize=(10, 5))
plt.plot(labels, values, marker='o', color='#7c3aed', label='Positive Sentiment %')
plt.title('LRCX MarketBeat Positive Sentiment Trend')
plt.xlabel('Month-Year')
plt.ylabel('Positive Sentiment (%)')
plt.xticks(rotation=45)
plt.ylim(0, 100)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.legend()
plt.savefig('lam_research_social_listening_dashboard/public/lrcx_marketbeat_positive_trend.png')
plt.close()
