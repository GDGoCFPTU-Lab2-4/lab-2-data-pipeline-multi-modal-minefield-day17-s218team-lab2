import re

import pandas as pd


# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Process sales records, handling type traps and duplicates.
def clean_price(val):
    if pd.isna(val):
        return 0.0

    val = str(val).lower().strip()

    if "five dollars" in val:
        return 5.0

    cleaned = re.sub(r"[^\d.-]", "", val)

    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def process_sales_csv(file_path):
    # --- FILE READING (Handled for students) ---
    df = pd.read_csv(file_path)
    # ------------------------------------------

    # TODO: Remove duplicate rows based on 'id'
    # TODO: Clean 'price' column: convert "$1200", "250000", "five dollars" to floats
    # TODO: Normalize 'date_of_sale' into a single format (YYYY-MM-DD)
    # TODO: Return a list of dictionaries for the UnifiedDocument schema.
    df = df.drop_duplicates(subset="id", keep="first")
    df["price"] = df["price"].apply(clean_price)
    df["date_of_sale"] = pd.to_datetime(
        df["date_of_sale"], errors="coerce", dayfirst=True
    )

    results = []
    for _, row in df.iterrows():
        # id,product_name,category,price,currency,date_of_sale,seller_id,stock_quantity
        content = f"Product: {row['product_name']}, Price: {row['price']}, Date: {row['date_of_sale']}"

        dt_str = None
        if pd.notna(row["date_of_sale"]):
            dt_str = row["date_of_sale"].strftime("%Y-%m-%d")

        doc = {
            "document_id": f"csv-{row['id']}",
            "content": content,
            "source_type": "CSV",
            "author": str(row["seller_id"]),
            "timestamp": dt_str,
            "source_metadata": {
                "original_file_id": int(row["id"]),
                "product_name": row["product_name"],
                "category": row["category"],
                "price": float(row["price"]),
                "currency": row["currency"],
                "stock_quantity": int(row["stock_quantity"])
                if pd.notna(row["stock_quantity"])
                else 0,
            },
        }
        results.append(doc)

    return results
