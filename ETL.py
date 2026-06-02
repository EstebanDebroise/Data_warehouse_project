import sqlite3
import pandas as pd
from datetime import datetime

# Configuration
SOURCE_DB = "data_bronze/social-media-advertisement-performance/ad_campaign_db.sqlite"
TARGET_DWH = "data_silver/analytics_dwh.sqlite"  # The new database for Superset


def extract(db_path: str) -> dict:
    """
    Step 1: Extract data from the source SQLite database.
    """
    print("--- Starting extraction ---")
    try:
        conn = sqlite3.connect(db_path)
        
        frames = {
            "ad_events": pd.read_sql_query("SELECT * FROM ad_events", conn),
            "users": pd.read_sql_query("SELECT * FROM users", conn),
            "ads": pd.read_sql_query("SELECT * FROM ads", conn),
            "campaigns": pd.read_sql_query("SELECT * FROM campaigns", conn)
        }
        
        conn.close()
        print(f"Extraction successful. {len(frames)} tables loaded into memory.")
        return frames
    except Exception as e:
        print(f"Error during extraction: {e}")
        raise


def transform(raw_data: dict) -> dict:
    """
    Step 2: Transform to a star schema.
    """
    print("--- Starting transformation ---")
    
    df_events = raw_data["ad_events"].copy()
    df_users = raw_data["users"].copy()
    df_ads = raw_data["ads"].copy()
    df_campaigns = raw_data["campaigns"].copy()

    # 1. Convert timestamps
    df_events['timestamp'] = pd.to_datetime(df_events['timestamp'])

    # 2. CREATE TIME DIMENSION (dim_date)
    print("Generating Time dimension...")
    unique_dates = df_events['timestamp'].dt.normalize().unique()
    
    dim_date = pd.DataFrame({'date_complete': unique_dates})
    dim_date['date_id'] = dim_date['date_complete'].dt.strftime('%Y%m%d').astype(int)
    dim_date['jour'] = dim_date['date_complete'].dt.day
    dim_date['mois'] = dim_date['date_complete'].dt.month
    dim_date['annee'] = dim_date['date_complete'].dt.year
    dim_date['trimestre'] = dim_date['date_complete'].dt.quarter
    dim_date['jour_semaine'] = dim_date['date_complete'].dt.day_name()
    dim_date['est_week_end'] = dim_date['date_complete'].dt.dayofweek.isin([5, 6]).astype(int)
    
    # Convert date_complete column to string for clean SQLite storage
    dim_date['date_complete'] = dim_date['date_complete'].dt.strftime('%Y-%m-%d')

    # 3. MERGE ADS AND CAMPAIGNS (flattened dim_ads)
    print("Merging ads and campaigns (Flattening)...")
    dim_ads = pd.merge(
        df_ads, 
        df_campaigns, 
        on="campaign_id", 
        how="left",
        suffixes=('', '_campaign')
    )

    # 4. FACTS TABLE STRUCTURE (fact_ad_events)
    print("Structuring the facts table...")
    df_events['date_id'] = df_events['timestamp'].dt.strftime('%Y%m%d').astype(int)
    
    fact_ad_events = df_events[[
        'event_id', 'ad_id', 'user_id', 'date_id', 'event_type'
    ]]
    
    dim_users = df_users.copy()

    print("Transformation completed successfully.")
    return {
        "fact_ad_events": fact_ad_events,
        "dim_users": dim_users,
        "dim_ads": dim_ads,
        "dim_date": dim_date
    }


def load(transformed_data: dict, target_db: str):
    """
    Step 3: Load into the new SQLite database (Data Warehouse).
    """
    print(f"--- Starting load into {target_db} ---")
    try:
        # Connection to the destination database (automatically created if it doesn't exist)
        conn = sqlite3.connect(target_db)
        
        for table_name, df in transformed_data.items():
            # if_exists='replace' allows you to overwrite the table if you re-run the script
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f"Table '{table_name}' injected ({len(df)} rows).")
            
        conn.close()
        print("--- ETL process completed successfully! ---")
    except Exception as e:
        print(f"Error during load: {e}")
        raise


# --- EXECUTION ---
if __name__ == "__main__":
    donnees_brutes = extract(SOURCE_DB)
    donnees_transformees = transform(donnees_brutes)
    load(donnees_transformees, TARGET_DWH)