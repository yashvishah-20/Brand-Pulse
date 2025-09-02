import pandas as pd
import json
from datetime import datetime
import os

def process_reddit_trends(excel_file_path, output_json_path):
    """
    Process Reddit Excel file to extract sentiment trends by month
    Date format: 29-05-2025 00:55:03
    """
    try:
        # Read the Excel file - try different sheets
        print("Checking available sheets in the Excel file...")
        excel_file = pd.ExcelFile(excel_file_path)
        print("Available sheets:", excel_file.sheet_names)
        
        # Try to read the first sheet
        df = pd.read_excel(excel_file_path, sheet_name=0)
        
        print("Columns in the Reddit Excel file:")
        print(df.columns.tolist())
        print("\nFirst 10 rows:")
        print(df.head(10))
        print("\nDataFrame shape:", df.shape)
        
        # Check if this looks like a pivot table - try other sheets
        for sheet_name in excel_file.sheet_names:
            print(f"\n--- Checking sheet: {sheet_name} ---")
            df_sheet = pd.read_excel(excel_file_path, sheet_name=sheet_name)
            print("Columns:", df_sheet.columns.tolist())
            print("First few rows:")
            print(df_sheet.head())
            
            # Check if this sheet has Date and Sentiment columns
            if 'Date' in df_sheet.columns and 'Sentiment' in df_sheet.columns:
                print(f"Found Date and Sentiment columns in sheet: {sheet_name}")
                df = df_sheet
                break
        
        # Final check if required columns exist
        if 'Date' not in df.columns or 'Sentiment' not in df.columns:
            print("Required columns 'Date' and 'Sentiment' not found in any sheet.")
            print("This might be a pivot table or summary format.")
            print("Available columns in the data:", df.columns.tolist())
            
            # Try to find if there's raw data in a different format
            # Look for columns that might contain dates or sentiments
            print("\nLooking for date-like or sentiment-like data...")
            for col in df.columns:
                print(f"Column '{col}' sample data:")
                print(df[col].dropna().head())
                print()
            
            return None
        # Format: 29-05-2025 00:55:03 (dd-mm-yyyy HH:MM:SS)
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y %H:%M:%S', errors='coerce')
        
        # Convert Date column to datetime with the specific format
        # Format: 29-05-2025 00:55:03 (dd-mm-yyyy HH:MM:SS)
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y %H:%M:%S', errors='coerce')
        
        # Filter out rows with invalid dates
        df = df.dropna(subset=['Date'])
        
        print(f"\nProcessed {len(df)} rows with valid dates")
        print("Date range:", df['Date'].min(), "to", df['Date'].max())
        print("Sentiment values:", df['Sentiment'].unique())
        
        # Group by month and sentiment, then count
        df['YearMonth'] = df['Date'].dt.to_period('M')
        sentiment_counts = df.groupby(['YearMonth', 'Sentiment']).size().unstack(fill_value=0)
        
        print("\nSentiment counts by month:")
        print(sentiment_counts)
        
        # Calculate percentages
        sentiment_percentages = sentiment_counts.div(sentiment_counts.sum(axis=1), axis=0) * 100
        
        # Prepare data for Chart.js
        labels = []
        positive_data = []
        neutral_data = []
        negative_data = []
        
        for period in sentiment_percentages.index:
            # Format as "MMM YYYY" (e.g., "Jan 2024")
            labels.append(period.strftime('%b %Y'))
            
            # Get percentages for each sentiment (round to 1 decimal place)
            positive_data.append(round(sentiment_percentages.loc[period].get('Positive', 0), 1))
            neutral_data.append(round(sentiment_percentages.loc[period].get('Neutral', 0), 1))
            negative_data.append(round(sentiment_percentages.loc[period].get('Negative', 0), 1))
        
        # Create the data structure for Chart.js
        chart_data = {
            "labels": labels,
            "positive": positive_data,
            "neutral": neutral_data,
            "negative": negative_data
        }
        
        # Save to JSON file
        with open(output_json_path, 'w') as f:
            json.dump(chart_data, f, indent=2)
        
        print(f"\nReddit trends data saved to: {output_json_path}")
        print(f"Data structure: {chart_data}")
        
        return chart_data
        
    except Exception as e:
        print(f"Error processing Reddit file: {e}")
        return None

if __name__ == "__main__":
    # Process Reddit data only
    reddit_excel_file = r"C:\Users\PraveenChaudhary\Desktop\data\LRCX_reddit_sentiment.xlsx"
    reddit_json_file = r"C:\Users\PraveenChaudhary\OneDrive - Prowess\Dipesh Solanki's files - Brand Pluse\lam_research_social_listening_dashboard\public\reddit_trends.json"
    
    print("Processing Reddit trends data...")
    reddit_result = process_reddit_trends(reddit_excel_file, reddit_json_file)
    
    if reddit_result:
        print("Reddit trends data processed successfully.")