import json
import matplotlib.pyplot as plt
from pathlib import Path

# Load the JSON data
json_path = Path('lam_research_social_listening_dashboard/public/lam_research_positive_sentiment.json')
with open(json_path, 'r') as f:
    data = json.load(f)

reddit_labels = data.get('reddit_labels', [])
reddit_values = data.get('reddit_positive', [])

plt.figure(figsize=(12, 6))
plt.plot(reddit_labels, reddit_values, marker='o', color='#ff4500', label='Lam Research Reddit Positive (Monthly Count)')
plt.title('Lam Research Reddit Positive Sentiment Trend')
plt.xlabel('Month-Year')
plt.ylabel('Positive Sentiment (Count)')
plt.xticks(rotation=45)
plt.ylim(0, max(reddit_values + [10]))
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.legend()
plt.savefig('lam_research_social_listening_dashboard/public/lam_research_reddit_positive_line_chart.png')
plt.close() 