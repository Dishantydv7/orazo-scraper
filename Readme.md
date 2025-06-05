# IndiaMart Multi-Category Scraper

## Purpose
This Python script (`main.py`) in Method 1 folder scrapes product and supplier details from multiple IndiaMart category pages, specified in `file.txt`. It extracts data such as price, description, company name, address, and contact details, saving the results to a single CSV file (`all_categories_combined.csv`) for analysis.

## Current Functionality
- **Input**: Reads category names from `file.txt` (one per line, e.g., `"Industrial Equipment & Components"`).
- **Process**:
  1. Constructs search URLs for each category (e.g., `https://dir.indiamart.com/search.mp?ss=Industrial+Supplies`).
  2. Fetches HTML using `requests` and parses it with `BeautifulSoup`.
  3. Extracts:
     - **Price**: From `p.price` (e.g., `₹ 1,500/Unit`).
     - **Description**: From `p.tac.wpw` (often contains addresses).
     - **Company Name**: From `div.companyname`.
     - **Seller Address**: From `span.cmpLoc`.
     - **Contact Details**: From `span.mobTxt` (often empty).
     - **Category**: From `file.txt`.
  4. Saves data to `all_categories_combined.csv` with a blank row between categories.
- **Output**: A CSV file with columns: `Price`, `Description`, `Company Name`, `Seller Address`, `Contact Details`, `Category`.

## Limitations
- **Category-Specific Selectors**: Relies on fixed HTML classes (e.g., `p.price`, `span.cmpLoc`), which may fail for categories with different structures.
- **Static Scraping**: Cannot extract dynamic content (e.g., phone numbers revealed via “Call” buttons).
- **Data Misalignment**: The `Description` field often contains addresses or unrelated text.
- **Anti-Scraping**: May be blocked by CAPTCHAs or rate limits, with no retry mechanism.

## Previous Iteration
The earlier script (`finalfinal.py`) in Method 2 folder was limited to scraping the Surgical Gloves category (`https://dir.indiamart.com/impcat/surgical-gloves.html`), saving HTML to `scrapedHtmlContent.txt` and data to `scrapedContent.csv`. It faced similar selector and static scraping limitations. `main.py` improves by supporting multiple categories via `file.txt` and combining outputs into one CSV.

## How to Run
1. Place `file.txt` with category names in the project directory.
2. Run:
   ```bash
   python main.py
   ```
3. Output: `all_categories_combined.csv`.