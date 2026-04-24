import json
import time
import os

# Robust path handling
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "raw_data")


# Import role-specific modules
from schema import UnifiedDocument
from process_pdf import extract_pdf_data
from process_transcript import clean_transcript
from process_html import parse_html_catalog
from process_csv import process_sales_csv
from process_legacy_code import extract_logic_from_code
from quality_check import run_quality_gate

# ==========================================
# ROLE 4: DEVOPS & INTEGRATION SPECIALIST
# ==========================================
# Task: Orchestrate the ingestion pipeline and handle errors/SLA.

def main():
    start_time = time.time()
    final_kb = []
    
    # --- FILE PATH SETUP (Handled for students) ---
    pdf_path = os.path.join(RAW_DATA_DIR, "lecture_notes.pdf")
    trans_path = os.path.join(RAW_DATA_DIR, "demo_transcript.txt")
    html_path = os.path.join(RAW_DATA_DIR, "product_catalog.html")
    csv_path = os.path.join(RAW_DATA_DIR, "sales_records.csv")
    code_path = os.path.join(RAW_DATA_DIR, "legacy_pipeline.py")
    
    output_path = os.path.join(os.path.dirname(SCRIPT_DIR), "processed_knowledge_base.json")
    # ----------------------------------------------

    # TODO: Call each processing function (extract_pdf_data, clean_transcript, etc.)
    # Định nghĩa danh sách các tác vụ cần thực hiện
    tasks = [
        ("PDF", extract_pdf_data, pdf_path),
        ("Transcript", clean_transcript, trans_path),
        ("HTML", parse_html_catalog, html_path),
        ("CSV", process_sales_csv, csv_path),
        ("Legacy Code", extract_logic_from_code, code_path)
    ]

    for name, func, path in tasks:
        print(f"Starting ingestion for: {name}...")
        try:
            # Gọi hàm xử lý
            result = func(path)
            
            if not result:
                continue

            # TODO: Run quality gates (run_quality_gate) before adding to final_kb
            # Xử lý kết quả (có thể là một danh sách hoặc một dictionary đơn lẻ)
            if isinstance(result, list):
                for doc_dict in result:
                    if run_quality_gate(doc_dict):
                        final_kb.append(doc_dict)
            else:
                if run_quality_gate(result):
                    final_kb.append(result)
                    
        except Exception as e:
            print(f"Error processing {name} from {path}: {e}")

    # TODO: Save final_kb to output_path using json.dump
    print(f"Saving {len(final_kb)} documents to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_kb, f, indent=4, ensure_ascii=False)

    end_time = time.time()
    print(f"Pipeline finished in {end_time - start_time:.2f} seconds.")
    print(f"Total valid documents stored: {len(final_kb)}")


if __name__ == "__main__":
    main()
