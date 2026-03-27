import os
import pandas as pd
from sqlalchemy import create_engine
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'   ]


# Save DataFrame ke CSV
def save_to_csv(df, filepath="products.csv"):
    try:
        if df is None or df.empty:
            raise ValueError("DataFrame kosong atau None.")
        
        df.to_csv(filepath, index=False)
        print(f"Data berhasil disimpan ke CSV :{filepath} ({len(df)} baris)")

    except Exception as e:
        print(f"CSV error: {e}")
        return False
    
    except Exception as e:
        print(f"Unexpected error saat menyimpan CSV: {e}")
        return False

# Create koneksi google Sheets API
def get_google_sheets_service(credentials_file="google-sheets-api.json"):
    try:
        creds = Credentials.from_service_account_file(credentials_file, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        return service
    
    except FileNotFoundError:
        print(f"File credentials tidak ditemukan: {credentials_file}")
        return None
    
    except Exception as e:
        print(f"Error koneksi Google Sheets: {e}")
        return None
    
# Save DataFrame ke Google Sheets
def save_to_google_sheets(df, spreadsheet_id, credentials_file="google-sheets-api.json"):
    try:
        if df is None or df.empty:
            raise ValueError("DataFrame kosong atau None.")
        
        if not spreadsheet_id:
            raise ValueError("Spreadsheet_ID tidak boleh kosong.")
        
        service = get_google_sheets_service(credentials_file)
        if service is None:
            raise ConnectionError("Gagal koneksi ke Google Sheets API.")
        
        values = [df.columns.tolist()] + df.astype(str).values.tolist()
        service.spreadsheets().values().clear(spreadsheetID=spreadsheet_id, range="Sheet1").execute()

        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range="Sheet1!A1",
            valueInputOption="RAW",
            body={"values": values}
        ).execute()

        print(f"Data berhasil disimpan ke Google Sheets ({result.get('updateRows')} baris)")
        return True
    
    except ValueError as e:
        print(f"google Sheets error: {e}")
        return False
    
    except ConnectionError as e:
        print(f"Google Sheets connection error: {e}")
        return False
    
    except Exception as e:
        print(f"Unexpected error saat menyimpan ke Google Sheets: {e}")
        return False
    
# Create koneksi postgreSQL
def get_postgres_engine(db_url):
    try:
        engine = create_engine(db_url)
        return engine
    except Exception as e:
        print(f"Error membuat koneksi PostgreSQL Engine: {e}")
        return None
    
# Save DataFrame ke PostgreSQL
def save_to_postgres(df, db_url, table_name="products"):
    try:
        if df is None or df.empty:
            raise ValueError("DataFrame kosong atau None.")
    
        engine = get_postgres_engine(db_url)
        if engine is None:
            raise ConnectionError("Gagal membuat PostgreSQL Engine.")
        
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Data berhasil disimpan ke PostgreSQL tabel '{table_name}' ({len(df)} baris)")
        return True
    
    except ValueError as e:
        print(f"PostgreSQL error: {e}")
        return False
    
    except ConnectionError as e:
        print(f"PostgreSQL connection error: {e}")
        return False
    
    except Exception as e:
        print(f"Unexpected error saat menyimpan ke PostgreSQL: {e}")
        return False

