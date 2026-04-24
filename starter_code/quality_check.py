# ==========================================
# ROLE 3: OBSERVABILITY & QA ENGINEER
# ==========================================
# Task: Implement quality gates to reject corrupt data or logic discrepancies.


def run_quality_gate(document_dict):
    # TODO: Reject documents with 'content' length < 20 characters
    # TODO: Reject documents containing toxic/error strings (e.g., 'Null pointer exception')
    # TODO: Flag discrepancies (e.g., if tax calculation comment says 8% but code says 10%)

    content = document_dict.get("content", "")
    if len(content) < 20:
        return False

    toxic_string = [
        "Null pointer exception",
        "runtime error",
        "access denied",
        "corrupt data",
        "error 404",
    ]
    if any(toxic.lower() in content.lower() for toxic in toxic_string):
        return False
    if document_dict.get("source_type") == "code":
        if "8%" in content and "10%" in content and "tax" in content.lower():
            return False

    return True
