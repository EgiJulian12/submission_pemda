from utils.extract import scrape_main
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_google_sheets, save_to_postgres

# Konfigurasi
SPREADSHEET_ID = "1uMbGB_QdMH2ZdeZ3aOsaJFgqn-z-5hlJTQ30UlmdHi4"
CREDENTIALS_FILE = "google-sheets-api.json"
DB_URL = "postgresql://postgres:Egijulian1_2@localhost:5432/fashion_db"
CSV_PATH = "products.csv"

# Run ETL pipeline
def run_pipeline():
    
    # Extract
    raw_data = scrape_main()

    if raw_data is None:
        print("Ekstraksi gagal. Pipeline dihentikan.")
        return
    
    print(f"Berhasil Mengekstrak {len(raw_data)} produk mentah.")

    # Transform
    clean_df = transform_data(raw_data)

    if clean_df is None or clean_df.empty:
        print("Transformasi gagal. Pipeline dihentikan.")
        return
    
    print(f"Transformasi berhasil. {len(clean_df)} baris data bersih.")
    print(clean_df.head())
    print(clean_df.dtypes)

    # Load ke CSV
    csv_ok = save_to_csv(clean_df, CSV_PATH)
    print(f" CSV Save: {'Sukses' if csv_ok else 'Gagal'}")

    # Load ke Google Sheets
    sheets_ok = save_to_google_sheets(clean_df, SPREADSHEET_ID, CREDENTIALS_FILE)
    print(f" Google Sheets Save: {'Sukses' if sheets_ok else 'Gagal'}")

    # Load ke PostgreSQL
    db_ok = save_to_postgres(clean_df, DB_URL)
    print(f" PostgreSQL Save: {'Sukses' if db_ok else 'Gagal'}")

if __name__ == "__main__":
    run_pipeline()