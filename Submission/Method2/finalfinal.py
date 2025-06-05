import requests
from bs4 import BeautifulSoup
import re
import csv

def fetch_and_save_html(url, output_path):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
    }
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(resp.text)
    print(f"✅ Saved HTML to '{output_path}'.")

def parse_products_from_html(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')

    # The main category (from meta or h1)
    category = None
    title_tag = soup.find('title')
    if title_tag:
        m = re.search(r'^(.*?)\s*[-|]', title_tag.text)
        if m:
            category = m.group(1).strip()
        else:
            category = title_tag.text.strip()

    products = []
    for li in soup.find_all('li', class_='lst'):
        # Product Name
        prod_name = ''
        prod_link = li.find('a', class_='smTle')
        if prod_link and prod_link.text.strip():
            prod_name = prod_link.text.strip()
        else:
            img = li.find('img')
            if img and img.get('alt'):
                prod_name = img['alt'].strip()

        # Supplier Name
        supplier = ''
        h2 = li.find('h2', class_='lcname')
        if h2 and h2.text.strip():
            supplier = h2.text.strip()
        else:
            a = li.find('a', href=True)
            if a and a.text.strip():
                supplier = a.text.strip()

        # Address (location)
        address = ''
        p = li.find('p', class_='sm clg')
        if p and p.text.strip():
            address = p.text.strip()
        else:
            address = li.get('data-location', '').strip()

        # Price
        price = ''
        price_span = li.find('span', class_='gtqte')
        if price_span and price_span.text.strip():
            price = price_span.text.strip()
        else:
            price_p = li.find('p', class_=re.compile('price'))
            if price_p and price_p.text.strip():
                price = price_p.text.strip()
            else:
                price_span2 = li.find('span', class_=re.compile('price'))
                if price_span2 and price_span2.text.strip():
                    price = price_span2.text.strip()

        if prod_name:
            products.append({
                'category': category,
                'product': prod_name,
                'supplier': supplier,
                'address': address,
                'price': price
            })
    return products

def save_products_to_csv(products, csv_path):
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['category', 'product', 'supplier', 'address', 'price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for prod in products:
            writer.writerow(prod)

if __name__ == "__main__":
    url = "https://dir.indiamart.com/impcat/surgical-gloves.html"
    html_path = "scrapedHtmlContent.txt"
    csv_path = "scrapedContent.csv"

    # Step 1: Download and save HTML
    fetch_and_save_html(url, html_path)

    # Step 2: Parse products from HTML
    products = parse_products_from_html(html_path)

    # Step 3: Save to CSV
    save_products_to_csv(products, csv_path)
    print(f"✅ Extracted {len(products)} products and saved to '{csv_path}'.")