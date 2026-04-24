import re

from bs4 import BeautifulSoup

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract product data from the HTML table, ignoring boilerplate.


def parse_html_catalog(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # ------------------------------------------

    # TODO: Use BeautifulSoup to find the table with id 'main-catalog'
    table = soup.find("table", id="main-catalog")
    if not table:
        return []
    # TODO: Extract rows, handling 'N/A' or 'Liên hệ' in the price column.
    results = []
    tbody = table.find("tbody")
    if not tbody:
        return []

    rows = tbody.find_all("tr")

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 6:
            continue

        sp_id = cols[0].text.strip()
        name = cols[1].text.strip()
        category = cols[2].text.strip()
        raw_price = cols[3].text.strip()
        stock = cols[4].text.strip()
        rating = cols[5].text.strip()

        # TODO: Return a list of dictionaries for the UnifiedDocument schema.
        price_val = 0.0
        if raw_price.lower() not in ["n/a", "liên hệ"]:
            cleaned_price = re.sub(r"[^\d.]", "", raw_price)
            if cleaned_price:
                price_val = float(cleaned_price)

        try:
            stock_val = int(stock)
        except ValueError:
            stock_val = 0

        content = f"Product: {name} ({sp_id}), Category: {category}, Price: {price_val}, Stock: {stock_val} VND, Rating: {rating}"

        doc = {
            "document_id": f"html_{sp_id}",
            "content": content,
            "source_type": "HTML",
            "author": "VinShop System",
            "timestamp": None,
            "source_metadata": {
                "product_id": sp_id,
                "product_name": name,
                "category": category,
                "price": price_val,
                "stock": stock_val,
                "rating": rating,
            },
        }
        results.append(doc)

    return results
