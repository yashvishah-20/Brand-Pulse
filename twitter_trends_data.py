import pandas as pd
import json
import os
from datetime import datetime
from collections import defaultdict

def process_twitter_data():
    """
    Process Twitter sentiment data from Excel file and generate trends JSON
    """
    # File paths
    excel_file = r"C:\Users\PraveenChaudhary\Desktop\data\LRCX_twitter_sentiment.xlsx"
    output_file = r"C:\Users\PraveenChaudhary\OneDrive - Prowess\Dipesh Solanki's files - Brand Pluse\lam_research_social_listening_dashboard\public\twitter_trends.json"
    
    print("🚀 Starting Twitter sentiment data processing...")
    
    try:
        # Read Excel file - specifically Sheet1
        print(f"📊 Reading Excel file: {excel_file}")
        print(f"📋 Using Sheet1...")
        df = pd.read_excel(excel_file, sheet_name='Sheet1')
        
        # Display basic info about the dataset
        print(f"✅ Data loaded successfully!")
        print(f"📈 Total records: {len(df)}")
        print(f"📅 Columns: {list(df.columns)}")
        
        # Check for required columns (case-insensitive search)
        date_column = None
        sentiment_column = None
        
        # Find date column (look for variations)
        for col in df.columns:
            if any(keyword in col.lower() for keyword in ['date', 'time', 'created']):
                date_column = col
                print(f"🔍 Found date column: '{col}'")
                break
        
        # Find sentiment column
        for col in df.columns:
            if 'sentiment' in col.lower():
                sentiment_column = col
                print(f"🔍 Found sentiment column: '{col}'")
                break
        
        if not date_column or not sentiment_column:
            print(f"❌ Missing required columns!")
            print(f"Available columns: {list(df.columns)}")
            print(f"Looking for: date/time column and sentiment column")
            return False
        
        # Display sample data
        print(f"\n📋 Sample data:")
        print(df[[date_column, sentiment_column]].head())
        
        # Check sentiment values
        print(f"\n🎯 Unique sentiment values: {df[sentiment_column].unique()}")
        print(f"📊 Sentiment distribution:")
        print(df[sentiment_column].value_counts())
        
        # Convert Date column to datetime - handle multiple date formats
        print(f"\n📅 Converting dates...")
        
        # Try different date formats
        date_formats = ['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d']
        
        converted = False
        for date_format in date_formats:
            try:
                df['parsed_date'] = pd.to_datetime(df[date_column], format=date_format)
                print(f"✅ Successfully parsed dates using format: {date_format}")
                converted = True
                break
            except:
                continue
        
        if not converted:
            try:
                # Try automatic date parsing
                df['parsed_date'] = pd.to_datetime(df[date_column], infer_datetime_format=True)
                print(f"✅ Successfully parsed dates using automatic detection")
            except Exception as e:
                print(f"❌ Failed to parse dates: {e}")
                print(f"Sample date values: {df[date_column].head()}")
                return False
        
        # Extract year-month for grouping
        df['YearMonth'] = df['parsed_date'].dt.to_period('M')
        
        print(f"📅 Date range: {df['parsed_date'].min()} to {df['parsed_date'].max()}")
        
        # Group by month and calculate sentiment percentages
        print(f"📈 Processing monthly sentiment trends...")
        monthly_data = defaultdict(lambda: {'positive': 0, 'neutral': 0, 'negative': 0, 'total': 0})
        
        for _, row in df.iterrows():
            month = row['YearMonth']
            sentiment = row[sentiment_column]
            
            # Handle different sentiment formats
            if pd.isna(sentiment):
                continue
                
            sentiment = str(sentiment).lower().strip()
            
            monthly_data[month]['total'] += 1
            
            if sentiment in ['positive', 'pos', '1', 'bullish', 'good']:
                monthly_data[month]['positive'] += 1
            elif sentiment in ['negative', 'neg', '-1', 'bearish', 'bad']:
                monthly_data[month]['negative'] += 1
            elif sentiment in ['neutral', 'neu', '0', 'mixed', 'neutral ']:
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
        
        print(f"✅ Twitter trends data saved successfully!")
        print(f"📊 Generated {len(labels)} data points from {df['parsed_date'].min().strftime('%Y-%m-%d')} to {df['parsed_date'].max().strftime('%Y-%m-%d')}")
        
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
            print(f"  Total tweets processed: {len(df)}")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Error: Excel file not found at {excel_file}")
        print("Please check the file path and ensure the file exists.")
        return False
    except Exception as e:
        print(f"❌ Error processing data: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def validate_output():
    """
    Validate the generated JSON file
    """
    output_file = r"C:\Users\PraveenChaudhary\OneDrive - Prowess\Dipesh Solanki's files - Brand Pluse\lam_research_social_listening_dashboard\public\twitter_trends.json"
    
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
        
        # Show sample data
        if data.get('labels'):
            print(f"\n📋 Sample data:")
            for i in range(min(3, len(data['labels']))):
                print(f"  {data['labels'][i]}: {data['positive'][i]}% pos, {data['neutral'][i]}% neu, {data['negative'][i]}% neg")
        
        return True
    except Exception as e:
        print(f"❌ JSON validation failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🐦 Twitter Sentiment Data Processor")
    print("=" * 60)
    
    # Process the data
    success = process_twitter_data()
    
    if success:
        # Validate the output
        validate_output()
        print(f"\n🎉 Processing completed successfully!")
        print(f"📁 Output file ready for use in the dashboard")
    else:
        print(f"\n❌ Processing failed. Please check the error messages above.")
    
    print("=" * 60)
