import PyPDF2

def extract_resume_text(filepath):
    """Extract raw text from a PDF resume."""
    text = ""
    with open(filepath, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return text.strip()
