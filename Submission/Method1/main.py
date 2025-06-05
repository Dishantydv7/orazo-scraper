import requests
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import quote_plus
import time

# Read categories from file.txt (one category per line)
with open("file.txt", "r", encoding="utf-8") as f:
    options = [line.strip() for line in f if line.strip()]

base_url = "https://dir.indiamart.com/search.mp?ss="

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
}

# Prepare the output file
output_file = "finalfinaloutput_csvs/all_categories_combined.csv"
os.makedirs("finalfinaloutput_csvs", exist_ok=True)
fieldnames = [
    "Price", "Description", "Company Name", "Seller Address", "Contact Details", "Category"
]

with open(output_file, "w", newline='', encoding='utf-8-sig') as fout:
    writer = csv.DictWriter(fout, fieldnames=fieldnames)
    writer.writeheader()

    for option in options:
        encoded_option = quote_plus(option)
        full_url = base_url + encoded_option
        print(f"Scraping: {option} → {full_url}")

        try:
            resp = requests.get(full_url, headers=headers, timeout=15)
            resp.raise_for_status()
        except Exception as e:
            print(f"Skipping {option} due to request error: {e}")
            continue

        soup = BeautifulSoup(resp.text, "html.parser")

        prices = soup.find_all('p', class_='price')
        descriptions = soup.find_all('p', class_='tac wpw')
        companies = soup.find_all('div', class_='companyname')
        addresses = soup.find_all('span', class_='cmpLoc')
        contacts = soup.find_all('span', class_='mobTxt')

        data = []
        max_len = max(len(prices), len(descriptions), len(companies), len(addresses), len(contacts))
        for i in range(max_len):
            price = prices[i].get_text(strip=True) if i < len(prices) else ""
            desc = descriptions[i].get_text(strip=True) if i < len(descriptions) else ""
            comp = companies[i].get_text(strip=True) if i < len(companies) else ""
            address = addresses[i].get_text(strip=True) if i < len(addresses) else ""
            contact = contacts[i].get_text(strip=True) if i < len(contacts) else ""
            writer.writerow({
                "Price": price,
                "Description": desc,
                "Company Name": comp,
                "Seller Address": address,
                "Contact Details": contact,
                "Category": option
            })
            print(comp)

        # Write a blank row to separate categories
        writer.writerow({})  # Blank line

        time.sleep(1)  # Be polite to the server

print(f"All categories scraped and saved to {output_file}.")