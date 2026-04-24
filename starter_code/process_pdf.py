import json
import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def extract_pdf_data(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None

    model = genai.GenerativeModel("gemini-1.5-flash")

    print(f"Uploading {file_path} to Gemini...")
    try:
        pdf_file = genai.upload_file(path=file_path)
    except Exception as e:
        print(f"Failed to upload file to Gemini: {e}")
        return None

    prompt = """
Analyze this document and extract a summary and the author.
Output exactly as a JSON object matching this exact format:
{
    "document_id": "pdf-doc-001",
    "content": "Summary: [Insert your 3-sentence summary here]",
    "source_type": "PDF",
    "author": "[Insert author name here]",
    "timestamp": null,
    "source_metadata": {"original_file": "lecture_notes.pdf"}
}
"""

    # Exponential Backoff implementation
    max_retries = 3
    retry_delay = 5  # Initial delay in seconds

    for attempt in range(max_retries):
        try:
            print(f"Generating content (Attempt {attempt + 1})...")
            response = model.generate_content([pdf_file, prompt])
            content_text = response.text
            
            # Simple cleanup
            if "```json" in content_text:
                content_text = content_text.split("```json")[1].split("```")[0]
            elif "```" in content_text:
                content_text = content_text.split("```")[1].split("```")[0]

            return json.loads(content_text.strip())
            
        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                print(f"Quota exceeded (429). Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential increase
            else:
                print(f"Failed to generate content: {e}")
                return None
    
    return None
