import pandas as pd
import json

# Path to the Excel file
data_path = r"C:\Users\PraveenChaudhary\Desktop\data\LRCX_reddit_sentiment.xlsx"

# Read the Excel file (Sheet1)
df = pd.read_excel(data_path, sheet_name="Sheet1")

# Sum the 'Upvotes' and 'Comments' columns, handling missing values
total_upvotes = df['Upvotes'].fillna(0).sum()
total_comments = df['Comments'].fillna(0).sum()

# Prepare the output JSON structure
output = {
    "reddit_activity": {
        "total_upvotes": int(total_upvotes),
        "total_comments": int(total_comments)
    }
}

# Write to JSON file in the dashboard public directory
with open(r"lam_research_social_listening_dashboard/public/reddit_activity_stats.json", "w") as f:
    json.dump(output, f, indent=2)
