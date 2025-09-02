import os
import json
import pandas as pd

# Mapping of company to their relevant Excel files (add more as needed)
company_files = {
    'Lam Research': [
        'data/Competitor/Marketbeat/AMAT_marketbeat_news_2025_2024_2023_processed.xlsx',
        'data/Competitor/Reddit/AMAT_reddit_sentiment.xlsx',
        'data/Competitor/StockTwits/stocktwits_AMAT_2025_2023_processed.xlsx',
        'data/Competitor/X (twitter)/AMAT_twitter_sentiment..xlsx',
        'data/Competitor/Linkedin/Applied Materials.xlsx',
    ],
    'Applied Materials': [
        'data/Competitor/Marketbeat/AMAT_marketbeat_news_2025_2024_2023_processed.xlsx',
        'data/Competitor/Reddit/AMAT_reddit_sentiment.xlsx',
        'data/Competitor/StockTwits/stocktwits_AMAT_2025_2023_processed.xlsx',
        'data/Competitor/X (twitter)/AMAT_twitter_sentiment..xlsx',
        'data/Competitor/Linkedin/Applied Materials.xlsx',
    ],
    'KLA Corporation': [
        'data/Competitor/Marketbeat/KLA_marketbeat_news_2025_2024_2023_porcessed.xlsx',
        'data/Competitor/Reddit/KLAC_reddit_sentiment.xlsx',
        'data/Competitor/StockTwits/stocktwits_KLAC_2025_2023_processed.xlsx',
        'data/Competitor/X (twitter)/KLAC_twitter_sentiment..xlsx',
        'data/Competitor/Linkedin/KLA Corp.xlsx',
    ],
    'Tokyo Electron': [
        'data/Competitor/Marketbeat/TOELY_marketbeat_news_2025_2024_2023_porcessed.xlsx',
        'data/Competitor/Reddit/TEL_reddit_sentiment.xlsx',
        'data/Competitor/StockTwits/stocktwits_TOELY_2025_2023_processed.xlsx',
        'data/Competitor/X (twitter)/TEL_twitter_sentiment.xlsx',
        # Add LinkedIn/Glassdoor if available
    ],
    'ASML Holding': [
        'data/Competitor/Marketbeat/ASML_marketbeat_news_2025_2024_2023_processed.xlsx',
        'data/Competitor/Reddit/ASML_reddit_sentiment.xlsx',
        'data/Competitor/StockTwits/stocktwits_ASML_2025_2023_processed.xlsx',
        'data/Competitor/X (twitter)/ASML_twitter_sentiment.xlsx',
        'data/Competitor/Linkedin/ASML.xlsx',
    ],
}

json_files = {
    'Lam Research': 'public/lam_research_positive_sentiment.json',
    'Applied Materials': 'public/amat_marketbeat_positive_sentiment.json',
    'KLA Corporation': 'public/kla_marketbeat_positive_sentiment.json',
    'Tokyo Electron': 'public/tokyo_electron_positive_sentiment.json',
    'ASML Holding': 'public/asml_positive_sentiment.json',
}

sentiments = ['positive', 'negative', 'neutral']

# Helper to extract year from a date string or pandas Timestamp
def extract_year(val):
    if pd.isnull(val):
        return None
    if isinstance(val, pd.Timestamp):
        return val.year
    try:
        return pd.to_datetime(val).year
    except Exception:
        return None

def aggregate_yearly_sentiments(files):
    yearly_counts = {}
    for file in files:
        if not os.path.exists(file):
            continue
        try:
            df = pd.read_excel(file, engine='openpyxl')
        except Exception:
            continue
        # Try to find columns for date/year and sentiment
        year_col = None
        for col in df.columns:
            if 'year' in col.lower() or 'date' in col.lower():
                year_col = col
                break
        if not year_col:
            continue
        # Try to find sentiment column
        sent_col = None
        for col in df.columns:
            if 'sentiment' in col.lower():
                sent_col = col
                break
        if not sent_col:
            continue
        # Group by year and sentiment
        df['year'] = df[year_col].apply(extract_year)
        for year, group in df.groupby('year'):
            if pd.isnull(year):
                continue
            if year not in yearly_counts:
                yearly_counts[year] = {s: 0 for s in sentiments}
            for s in sentiments:
                yearly_counts[year][s] += (group[sent_col].str.lower() == s).sum()
    return yearly_counts

def to_percentages(yearly_counts):
    years = sorted(yearly_counts.keys())
    pos, neg, neu = [], [], []
    for y in years:
        total = sum(yearly_counts[y].values())
        if total == 0:
            pos.append(0)
            neg.append(0)
            neu.append(0)
        else:
            pos.append(round(100 * yearly_counts[y]['positive'] / total, 2))
            neg.append(round(100 * yearly_counts[y]['negative'] / total, 2))
            neu.append(round(100 * yearly_counts[y]['neutral'] / total, 2))
    return years, pos, neg, neu

for company, files in company_files.items():
    yearly_counts = aggregate_yearly_sentiments(files)
    years, pos, neg, neu = to_percentages(yearly_counts)
    json_path = os.path.join(os.path.dirname(__file__), json_files[company])
    if not os.path.exists(json_path):
        print(f"JSON file not found for {company}: {json_path}")
        continue
    with open(json_path, 'r') as f:
        data = json.load(f)
    data['yearly_labels'] = [str(y) for y in years]
    data['yearly_positive'] = pos
    data['yearly_negative'] = neg
    data['yearly_neutral'] = neu
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Updated {company}: {years}") 