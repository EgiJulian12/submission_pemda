import pandas as pd

exchange_rate = 16000

# Konversi dolar ke rupiah
def convert_price(price_str):
    try:
        if price_str is None:
            return None
        price_str = str(price_str).strip()
        if price_str == "Price Unavailable" or price_str == "":
            return None
        cleaned = price_str.replace("$", "").replace(",","").strip()
        return float(cleaned) * exchange_rate
    
    except Exception as e :
        print(f"Error converting price '{price_str}': {e}")
        return None
    
# Konversi Rating
def convert_rating(rating_str):
    try:
        if rating_str is None:
            return None
        rating_str = str(rating_str).strip()
        if "Invalid Rating" in rating_str or "Not Rated" in rating_str:
            return None
        rating_str = rating_str.replace("⭐", "").strip()
        return float(rating_str.split("/")[0].strip)
    
    except Exception as e :
        print(f"Error converting rating '{rating_str}': {e}")
        return None
    
# Konversi color
def convert_colors(color_str):
    try:
        if color_str is None:
            return None
        return int(str(color_str).strip().split()[0])
    
    except Exception as e:
        print(f"Error converting colors '{color_str}': {e}")
        return None
    
# Konversi size
def convert_size(size_str):
    try:
        if size_str is None:
            return None
        return str(size_str).replace("Size:", "").strip()
    
    except Exception as e:
        print(f"Error converting size '{size_str}': {e}")
        return None

# Konversi gender
def convert_gender(gender_str):
    try:
        if gender_str is None:
            return None
        return str(gender_str).replace("Gender:", "").strip()
    
    except Exception as e:
        print(f"Error converting gender '{gender_str}': {e}")
        return None

# Transformasi data
def transform_data(raw_products):
    try:
        if raw_products is None:
            return ValueError("Input data adalah None.")
        
        df = pd.DataFrame(raw_products)

        if df.empty:
            raise ValueError("DataFrame Kosong.")
        
        # Konversi setiap kolom
        df["Price"] = df["Price"].apply(convert_price)
        df["Rating"] = df["Rating"].apply(convert_rating)
        df["Colors"] = df["Colors"].apply(convert_colors)
        df["Size"] = df["Size"].apply(convert_size)
        df["Gender"] = df["Gender"].apply(convert_gender)

        # Hapus baris 'Unknown Product'
        df = df[df["Tittle"] != "Unknown Product"]

        # Hapus baris Null
        df = df.dropna()

        # Hapus duplikat
        df = df.drop_duplicates()

        # Reset index
        df = df.reset_index(drop=True)

        # Memastikan tipe data sesuai
        df["Title"]  = df["Title"].astype(str)
        df["Price"]  = df["Price"].astype(float)
        df["Rating"] = df["Rating"].astype(float)
        df["Colors"] = df["Colors"].astype(int)
        df["Size"]   = df["Size"].astype(str)
        df["Gender"] = df["Gender"].astype(str)


        print(f"Transformasi Selesai. {len(df)} baris data bersih.")
        return df
    
    except ValueError as e:
        print(f"Transform Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None