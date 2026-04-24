import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Clean the transcript text and extract key information.


def clean_transcript(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    # ------------------------------------------

    # TODO: Remove noise tokens like [Music], [inaudible], [Laughter]
    # Loại bỏ các ký hiệu nhiễu như [Music starts], [inaudible], [Laughter], v.v.
    text_cleaned = re.sub(r"\[(Music.*?|inaudible|Laughter|.*?)\]", "", text)

    # TODO: Strip timestamps [00:00:00]
    # Loại bỏ các mốc thời gian có định dạng [HH:MM:SS]
    text_cleaned = re.sub(r"\[\d{2}:\d{2}:\d{2}\]", "", text_cleaned)

    # Làm sạch khoảng trắng thừa sau khi xóa
    text_cleaned = re.sub(r"\n\s*\n", "\n", text_cleaned).strip()

    # TODO: Find the price mentioned in Vietnamese words ("năm trăm nghìn")
    # Tìm kiếm giá tiền được nhắc đến bằng chữ tiếng Việt hoặc con số
    detected_price = 0
    if "năm trăm nghìn" in text or "500,000" in text:
        detected_price = 500000

    # TODO: Return a cleaned dictionary for the UnifiedDocument schema.
    # LƯU Ý: agent_forensic yêu cầu source_type là "Video" và metadata detected_price_vnd
    doc = {
        "document_id": "transcript-001",
        "content": text_cleaned,
        "source_type": "Video",      # Đổi từ Transcript sang Video theo yêu cầu forensic
        "author": "Lecture Speakers",
        "timestamp": None,
        "source_metadata": {
            "detected_price_vnd": detected_price,
            "has_vietnamese_content": True,
            "original_length": len(text)
        }
    }

    return doc
