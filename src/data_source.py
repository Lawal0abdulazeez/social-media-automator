# src/data_source.py
import pandas as pd
from datetime import datetime
import logging

def get_todays_post():
    """Fetch today's post from the CSV file."""
    try:
        # Read the CSV file directly
        df = pd.read_csv('acme.csv')

        today = datetime.now()
        today_str = f"{today.month}/{today.day}/{today.year}"

        logging.info(f"Today's date: {today_str}")
        
        # Make sure 'Date' column is in string format
        df['Date'] = df['Date'].astype(str)
        logging.info(f"CSV Data: {df}")

        # Find today's post
        todays_post_df = df[df['Date'] == today_str]
        logging.info(f"Today's post data: {todays_post_df}")
        
        if not todays_post_df.empty:
            return todays_post_df.to_dict('records')[0]
        return None
        
    except Exception as e:
        #print(f": {e}")
        print(f"Error reading CSV file: {e}")
        return None