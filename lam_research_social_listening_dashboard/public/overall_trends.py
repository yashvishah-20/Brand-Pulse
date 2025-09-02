import json
import os
from collections import defaultdict

# Paths to platform trend files
platform_files = [
    'reddit_trends.json',
    'marketbeat_trends.json',
    'stocktwits_trends.json',
    'twitter_trends.json'
]

# Directory where this script is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Load all data
platform_data = []
for fname in platform_files:
    fpath = os.path.join(base_dir, fname)
    with open(fpath, 'r') as f:
        platform_data.append(json.load(f))

# Collect all unique labels (months)
all_labels = set()
for data in platform_data:
    all_labels.update(data['labels'])

# Map month names to numbers for sorting
month_map = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
def label_sort_key(label):
    month, year = label.split()
    return (int(year), month_map[month])
all_labels = sorted(all_labels, key=label_sort_key)

# Aggregate sentiment for each label
overall = {'labels': [], 'positive': [], 'neutral': [], 'negative': []}
for label in all_labels:
    pos, neu, neg, count = 0, 0, 0, 0
    for data in platform_data:
        if label in data['labels']:
            idx = data['labels'].index(label)
            pos += data['positive'][idx]
            neu += data['neutral'][idx]
            neg += data['negative'][idx]
            count += 1
    if count > 0:
        overall['labels'].append(label)
        overall['positive'].append(round(pos/count, 2))
        overall['neutral'].append(round(neu/count, 2))
        overall['negative'].append(round(neg/count, 2))

# Write to overall_trends.json
with open(os.path.join(base_dir, 'overall_trends.json'), 'w') as f:
    json.dump(overall, f, indent=2) 