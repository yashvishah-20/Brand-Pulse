import os
import pandas as pd
import json

# Define the mapping of company names to their relevant Excel files (relative to the data/Competitor/ subfolders)
companies = {
    'Applied Materials': {
        'Marketbeat': 'Marketbeat/AMAT_marketbeat_news_2025_2024_2023_processed.xlsx',
        'Reddit': 'Reddit/AMAT_reddit_sentiment.xlsx',
        'StockTwits': 'StockTwits/stocktwits_AMAT_2025_2023_processed.xlsx',
        'Twitter': 'X (twitter)/AMAT_twitter_sentiment..xlsx',
        'LinkedIn': 'Linkedin/Applied Materials.xlsx',
    },
    'ASML Holding': {
        'Marketbeat': 'Marketbeat/ASML_marketbeat_news_2025_2024_2023_processed.xlsx',
        'Reddit': 'Reddit/ASML_reddit_sentiment.xlsx',
        'StockTwits': 'StockTwits/stocktwits_ASML_2025_2023_processed.xlsx',
        'Twitter': 'X (twitter)/ASML_twitter_sentiment.xlsx',
        'LinkedIn': 'Linkedin/ASML.xlsx',
    },
    'KLA Corporation': {
        'Marketbeat': 'Marketbeat/KLA_marketbeat_news_2025_2024_2023_porcessed.xlsx',
        'Reddit': 'Reddit/KLAC_reddit_sentiment.xlsx',
        'StockTwits': 'StockTwits/stocktwits_KLAC_2025_2023_processed.xlsx',
        'Twitter': 'X (twitter)/KLAC_twitter_sentiment..xlsx',
        'LinkedIn': 'Linkedin/KLA Corp.xlsx',
    },
    'Tokyo Electron': {
        'Marketbeat': 'Marketbeat/TOELY_marketbeat_news_2025_2024_2023_porcessed.xlsx',
        'Reddit': 'Reddit/TEL_reddit_sentiment.xlsx',
        'StockTwits': 'StockTwits/stocktwits_TOELY_2025_2023_processed.xlsx',
        'Twitter': 'X (twitter)/TEL_twitter_sentiment.xlsx',
        'LinkedIn': 'Linkedin/tokyo_electron_linkedin_posts_all_MAIN.csv',
    },
}

# Lam Research (A) files are in the main data folder
lam_files = [
    '../../LRCX_marketbeat_news.xlsx',
    '../../LRCX_reddit_sentiment.xlsx',
    '../../LRCX_stocktwits_sentiment.xlsx',
    '../../LRCX_twitter_sentiment.xlsx',
    '../../LRCX_Linkedin_company_posts.xlsx',
]

base_dir = os.path.join('brandmeter', "Dipesh Solanki's files - Brand Pluse", 'data', 'Competitor')

# Helper to count rows in Excel/CSV
def count_rows(filepath):
    if not os.path.exists(filepath):
        return 0
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)
    return len(df)

# Calculate total volumes
totals = {}

# Lam Research
lam_base = os.path.join('brandmeter', "Dipesh Solanki's files - Brand Pluse", 'data')
lam_total = 0
for rel_path in lam_files:
    full_path = os.path.join(lam_base, rel_path)
    lam_total += count_rows(full_path)
totals['Lam Research'] = lam_total

# Other companies
for company, files in companies.items():
    total = 0
    for rel_path in files.values():
        full_path = os.path.join(base_dir, rel_path)
        total += count_rows(full_path)
    totals[company] = total

# Write to JSON
json_path = os.path.join('brandmeter', "Dipesh Solanki's files - Brand Pluse", 'lam_research_social_listening_dashboard', 'public', 'total_volumes.json')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(totals, f, indent=2)

print('Updated total_volumes.json:', totals) 