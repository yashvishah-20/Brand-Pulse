import pandas as pd
import json
import os
from datetime import datetime
from collections import defaultdict

def process_stocktwits_data():
    """
    Process StockTwits sentiment data from Excel file and generate trends JSON
    """
    # File paths
    excel_file = r"C:\Users\PraveenChaudhary\Desktop\data\LRCX_stocktwits_sentiment.xlsx"
    output_file = r"C:\Users\PraveenChaudhary\OneDrive - Prowess\Dipesh Solanki's files - Brand Pluse\lam_research_social_listening_dashboard\public\stocktwits_trends.json"
    
    print("🚀 Starting StockTwits sentiment data processing...")
    
    try:
        # Read Excel file
        print(f"📊 Reading Excel file: {excel_file}")
        df = pd.read_excel(excel_file)
        
        # Display basic info about the dataset
        print(f"✅ Data loaded successfully!")
        print(f"📈 Total records: {len(df)}")
        print(f"📅 Columns: {list(df.columns)}")
        
        # Check for required columns
        required_columns = ['Date', 'Sentiment']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"❌ Missing required columns: {missing_columns}")
            print(f"Available columns: {list(df.columns)}")
            return False
        
        # Display sample data
        print("\n📋 Sample data:")
        print(df.head())
        
        # Check sentiment values
        print(f"\n🎯 Unique sentiment values: {df['Sentiment'].unique()}")
        print(f"📊 Sentiment distribution:")
        print(df['Sentiment'].value_counts())
        
        # Convert Date column to datetime
        print(f"\n📅 Converting dates...")
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Extract year-month for grouping
        df['YearMonth'] = df['Date'].dt.to_period('M')
        
        # Group by month and calculate sentiment percentages
        print(f"📈 Processing monthly sentiment trends...")
        monthly_data = defaultdict(lambda: {'positive': 0, 'neutral': 0, 'negative': 0, 'total': 0})
        
        for _, row in df.iterrows():
            month = row['YearMonth']
            sentiment = row['Sentiment'].lower().strip()
            
            monthly_data[month]['total'] += 1
            
            if sentiment in ['positive', 'pos']:
                monthly_data[month]['positive'] += 1
            elif sentiment in ['negative', 'neg']:
                monthly_data[month]['negative'] += 1
            elif sentiment in ['neutral', 'neu']:
                monthly_data[month]['neutral'] += 1
            else:
                print(f"⚠️ Unknown sentiment value: '{sentiment}' - treating as neutral")
                monthly_data[month]['neutral'] += 1
        
        # Convert to percentages and prepare data for JSON
        labels = []
        positive_percentages = []
        neutral_percentages = []
        negative_percentages = []
        
        # Sort months chronologically
        sorted_months = sorted(monthly_data.keys())
        
        print(f"\n📊 Monthly sentiment analysis:")
        for month in sorted_months:
            data = monthly_data[month]
            total = data['total']
            
            if total > 0:
                pos_pct = round((data['positive'] / total) * 100, 1)
                neu_pct = round((data['neutral'] / total) * 100, 1)
                neg_pct = round((data['negative'] / total) * 100, 1)
                
                # Format month label
                month_str = month.strftime('%b %Y')
                
                labels.append(month_str)
                positive_percentages.append(pos_pct)
                neutral_percentages.append(neu_pct)
                negative_percentages.append(neg_pct)
                
                print(f"  {month_str}: {pos_pct}% pos, {neu_pct}% neu, {neg_pct}% neg (total: {total})")
        
        # Create JSON structure
        trends_data = {
            "labels": labels,
            "positive": positive_percentages,
            "neutral": neutral_percentages,
            "negative": negative_percentages
        }
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Save to JSON file
        print(f"\n💾 Saving trends data to: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(trends_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ StockTwits trends data saved successfully!")
        print(f"📊 Generated {len(labels)} data points from {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")
        
        # Summary statistics
        if positive_percentages:
            avg_positive = sum(positive_percentages) / len(positive_percentages)
            max_positive = max(positive_percentages)
            min_positive = min(positive_percentages)
            
            print(f"\n📈 Summary Statistics:")
            print(f"  Average positive sentiment: {avg_positive:.1f}%")
            print(f"  Highest positive sentiment: {max_positive:.1f}%")
            print(f"  Lowest positive sentiment: {min_positive:.1f}%")
            print(f"  Data points: {len(labels)}")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Error: Excel file not found at {excel_file}")
        print("Please check the file path and ensure the file exists.")
        return False
    except Exception as e:
        print(f"❌ Error processing data: {str(e)}")
        return False

def validate_output():
    """
    Validate the generated JSON file
    """
    output_file = r"C:\Users\PraveenChaudhary\OneDrive - Prowess\Dipesh Solanki's files - Brand Pluse\lam_research_social_listening_dashboard\public\stocktwits_trends.json"
    
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"\n✅ JSON validation successful!")
        print(f"📊 Data structure:")
        print(f"  - Labels: {len(data.get('labels', []))} items")
        print(f"  - Positive: {len(data.get('positive', []))} items")
        print(f"  - Neutral: {len(data.get('neutral', []))} items")
        print(f"  - Negative: {len(data.get('negative', []))} items")
        
        # Check if all arrays have the same length
        lengths = [len(data.get(key, [])) for key in ['labels', 'positive', 'neutral', 'negative']]
        if len(set(lengths)) == 1:
            print(f"✅ All data arrays have consistent length: {lengths[0]}")
        else:
            print(f"⚠️ Inconsistent array lengths: {lengths}")
        
        return True
    except Exception as e:
        print(f"❌ JSON validation failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🎯 StockTwits Sentiment Data Processor")
    print("=" * 60)
    
    # Process the data
    success = process_stocktwits_data()
    
    if success:
        # Validate the output
        validate_output()
        print(f"\n🎉 Processing completed successfully!")
        print(f"📁 Output file ready for use in the dashboard")
    else:
        print(f"\n❌ Processing failed. Please check the error messages above.")
    
    print("=" * 60)
