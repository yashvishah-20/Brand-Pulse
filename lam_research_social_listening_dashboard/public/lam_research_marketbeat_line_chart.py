import json
import matplotlib.pyplot as plt
from pathlib import Path

# Load the JSON data
json_path = Path('lam_research_social_listening_dashboard/public/lam_research_positive_sentiment.json')
with open(json_path, 'r') as f:
    data = json.load(f)

labels = data['labels']
values = data['positive']
reddit_labels = data.get('reddit_labels', [])
reddit_values = data.get('reddit_positive', [])

plt.figure(figsize=(12, 6))
plt.plot(labels, values, marker='o', color='#7c3aed', label='Lam Research MarketBeat Positive %')
if reddit_labels and reddit_values:
    plt.plot(reddit_labels, reddit_values, marker='s', color='#ff4500', linestyle='--', label='Lam Research Reddit Positive (Monthly Count)')
plt.title('Lam Research Positive Sentiment Trend')
plt.xlabel('Month-Year')
plt.ylabel('Positive Sentiment (%) or Count')
plt.xticks(rotation=45)
plt.ylim(0, max([v for v in (values + reddit_values) if v is not None] + [100]))
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.legend()
plt.savefig('lam_research_social_listening_dashboard/public/lam_research_marketbeat_line_chart.png')
plt.close() 