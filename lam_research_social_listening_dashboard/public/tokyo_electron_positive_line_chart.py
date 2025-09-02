import json
import matplotlib.pyplot as plt
from pathlib import Path

# Load the JSON data
json_path = Path('lam_research_social_listening_dashboard/public/tokyo_electron_positive_sentiment.json')
with open(json_path, 'r') as f:
    data = json.load(f)

labels = data['labels']
values = data['positive']

plt.figure(figsize=(10, 5))
plt.plot(labels, values, marker='o', color='#E67E22', label='Tokyo Electron (TOELY)')
plt.title('Tokyo Electron Positive Sentiment Trend')
plt.xlabel('Month-Year')
plt.ylabel('Positive Sentiment (%)')
plt.xticks(rotation=45)
plt.ylim(0, 100)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.legend()
plt.savefig('lam_research_social_listening_dashboard/public/tokyo_electron_positive_line_chart.png')
plt.close() 