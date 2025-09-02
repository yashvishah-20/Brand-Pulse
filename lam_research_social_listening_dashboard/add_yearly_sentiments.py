import json
import os

# List of JSON files to update
files = [
    'public/lam_research_positive_sentiment.json',
    'public/amat_marketbeat_positive_sentiment.json',
    'public/kla_marketbeat_positive_sentiment.json',
    'public/tokyo_electron_positive_sentiment.json',
    'public/asml_positive_sentiment.json'
]

# Dummy values for negative and neutral (can be randomized or set as needed)
def generate_dummy_sentiments(length, positive):
    # Ensure total is 100, split remaining between negative and neutral
    negative = [round((100 - p) * 0.4, 2) for p in positive]
    neutral = [round(100 - p - n, 2) for p, n in zip(positive, negative)]
    return negative, neutral

for file in files:
    path = os.path.join(os.path.dirname(__file__), file)
    with open(path, 'r') as f:
        data = json.load(f)
    yearly_labels = data.get('yearly_labels', [])
    positive = data.get('yearly_positive', [0]*len(yearly_labels))
    if not yearly_labels or not positive:
        print(f"Skipping {file}: missing yearly_labels or yearly_positive")
        continue
    negative, neutral = generate_dummy_sentiments(len(yearly_labels), positive)
    data['yearly_negative'] = negative
    data['yearly_neutral'] = neutral
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Updated {file}: Added yearly_negative and yearly_neutral.") 