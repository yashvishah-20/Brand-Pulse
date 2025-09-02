import pandas as pd
import json
from collections import Counter
from datetime import datetime

# Path to the Excel file
excel_path = r"C:\Users\PraveenChaudhary\Desktop\data\LRCX_reddit_sentiment.xlsx"

# Read the Excel file (Sheet1)
df = pd.read_excel(excel_path, sheet_name='Sheet1')

def get_peak_hours(date_series):
    # Parse the date strings and extract hour
    hours = []
    for date_str in date_series:
        try:
            # Try parsing as string in format 'YYYY-MM-DD HH:MM:SS'
            dt = None
            if isinstance(date_str, str):
                dt = datetime.strptime(date_str.strip(), '%Y-%m-%d %H:%M:%S')
            else:
                # If it's already a datetime object (from pandas), just use it
                dt = pd.to_datetime(date_str)
            hours.append(dt.hour)
        except Exception:
            continue
    # Count frequency of each hour
    hour_counts = Counter(hours)
    # Group into time slots
    slots = {
        '0-3 AM': 0, '3-6 AM': 0, '6-9 AM': 0, '9-12 AM': 0,
        '12-3 PM': 0, '3-6 PM': 0, '6-9 PM': 0, '9-12 PM': 0
    }
    for hour, count in hour_counts.items():
        if 0 <= hour < 3:
            slots['0-3 AM'] += count
        elif 3 <= hour < 6:
            slots['3-6 AM'] += count
        elif 6 <= hour < 9:
            slots['6-9 AM'] += count
        elif 9 <= hour < 12:
            slots['9-12 AM'] += count
        elif 12 <= hour < 15:
            slots['12-3 PM'] += count
        elif 15 <= hour < 18:
            slots['3-6 PM'] += count
        elif 18 <= hour < 21:
            slots['6-9 PM'] += count
        elif 21 <= hour < 24:
            slots['9-12 PM'] += count
    return slots

# Extract peak hours
time_slots = get_peak_hours(df['Date'])

# Prepare output JSON
output = {
    'peak_hours': [
        {'slot': slot, 'count': count} for slot, count in time_slots.items()
    ]
}

# Save to JSON file
with open(r"C:\Users\PraveenChaudhary\OneDrive - Prowess\Dipesh Solanki's files - Brand Pluse\lam_research_social_listening_dashboard\public\reddit_peak_hours.json", 'w') as f:
    json.dump(output, f, indent=2)

print('Reddit peak hours data saved to reddit_peak_hours.json')
