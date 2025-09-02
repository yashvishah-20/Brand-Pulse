import pandas as pd

# Load the data
file = r'C:/Users/YashviShah/Downloads/StockTwits/StockTwits/stocktwits_ASML_2025_2023_processed.xlsx'
df = pd.read_excel(file)
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Sentiment'] = df['Sentiment'].str.lower()

for year in [2023, 2024, 2025]:
    year_df = df[df['Date'].dt.year == year]
    pos = (year_df['Sentiment'] == 'positive').sum()
    total = year_df['Sentiment'].isin(['positive', 'negative']).sum()
    pct = (pos / total * 100) if total else 0
    print(f'{year}: {pos}/{total} = {pct:.2f}%') 