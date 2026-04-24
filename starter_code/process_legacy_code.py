import ast
import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract docstrings and comments from legacy Python code.

def extract_logic_from_code(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    # ------------------------------------------
    
    # TODO: Use the 'ast' module to find docstrings for functions
    tree = ast.parse(source_code)
    
    extracted_info = []
    
    # Lấy docstring của Module (đầu file)
    module_doc = ast.get_docstring(tree)
    if module_doc:
        extracted_info.append(f"Module Documentation:\n{module_doc}")
    
    # Duyệt qua các hàm để lấy docstring
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            doc = ast.get_docstring(node)
            if doc:
                extracted_info.append(f"Function '{node.name}' Logic:\n{doc}")
            else:
                extracted_info.append(f"Function '{node.name}' has no docstring.")

    # TODO: (Optional/Advanced) Use regex to find business rules in comments like "# Business Logic Rule 001"
    # Tìm kiếm các quy tắc nghiệp vụ trong comment
    comments = re.findall(r'#.*', source_code)
    if comments:
        extracted_info.append("Business Rules in Comments:")
        for comment in comments:
            # Lọc các comment có chứa từ khóa quan trọng
            if any(key in comment.lower() for key in ["rule", "logic", "warning", "important", "check"]):
                extracted_info.append(f"- {comment.strip()}")

    # TODO: Return a dictionary for the UnifiedDocument schema.
    full_content = "\n\n".join(extracted_info)
    
    doc = {
        "document_id": "legacy-code-001",
        "content": full_content,
        "source_type": "Code",
        "author": "Legacy System",
        "timestamp": None,
        "source_metadata": {
            "file_name": file_path.split("/")[-1],
            "function_count": len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]),
            "has_docstrings": module_doc is not None
        }
    }
    
    return doc
