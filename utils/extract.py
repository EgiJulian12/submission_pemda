import requests
from bs4 import BeautifulSoup
from datetime import datetime

BASE_URL = "https://fashion-studio.dicoding.dev/"

# Mengambil konten HTML
def fetch_page(session, url):
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {url}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


# Mengekstrak data produk
def parse_products(html_content):
    if html_content is None:
        return []

    try:
        soup = BeautifulSoup(html_content, "html.parser")
        products = []
        timestamp = datetime.now().isoformat()

        cards = soup.find_all("div", class_="collection-card")

        for card in cards:
            try:
                details = card.find("div", class_="product-details")
                if not details:
                    continue

                # Ambil Title
                title_tag = details.find("h3", class_="product-title")
                title = title_tag.text.strip() if title_tag else None

                # Ambil Price
                price_tag = details.find("span", class_="price")
                price = price_tag.text.strip() if price_tag else None

                # Ambil Rating, Colors, Size, Gender dari tag <p>
                rating = colors = size = gender = None
                for p in details.find_all("p"):
                    text = p.text.strip()
                    if "Rating:" in text:
                        rating = text.replace("Rating:", "").strip()
                    elif "Colors" in text:
                        colors = text
                    elif "Size:" in text:
                        size = text
                    elif "Gender:" in text:
                        gender = text

                products.append({
                    "Title": title,
                    "Price": price,
                    "Rating": rating,
                    "Colors": colors,
                    "Size": size,
                    "Gender": gender,
                    "Timestamp": timestamp,
                })

            except Exception as e:
                print(f"Error parsing card: {e}")
                continue

        return products

    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return []


# Scraping semua halaman dan mengembalikan list produk.
def scrape_main(url=BASE_URL, start_page=1):
    products = []

    try:
        session = requests.Session()

        for page in range(start_page, 51):
            page_url = url if page == 1 else f"{url}page{page}"
            print(f"Scraping halaman {page}: {page_url}")

            html = fetch_page(session, page_url)
            if html is None:
                print(f"  → Halaman {page} dilewati.")
                continue

            page_products = parse_products(html)
            products.extend(page_products)
            print(f"  → {len(page_products)} produk ditemukan.")

        return products

    except requests.exceptions.RequestException as e:
        print(f"Error fetching website: {e}")
        return None
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return None