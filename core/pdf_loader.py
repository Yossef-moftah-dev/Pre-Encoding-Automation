#############################################################
####                    PDF text extraction module.
#############################################################
import io
from pypdf import PdfReader


def extract_text_from_pdf(pdf_file) -> str:
    # Extract text from a text-native PDF.
    # Args:
    #     pdf_file: File-like object or path to PDF.
    # Returns:
    #     Extracted text as string.
    # Raises:
    #     ValueError: If PDF is empty or unreadable.

    if isinstance(pdf_file, str):
        with open(pdf_file, 'rb') as f:
            pdf_bytes = f.read()
    else:
        pdf_bytes = pdf_file.read() if hasattr(pdf_file, 'read') else pdf_file
    
    reader = PdfReader(io.BytesIO(pdf_bytes))
    
    if not reader.pages:
        raise ValueError("PDF contains no pages")
    
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    
    if not text.strip():
        raise ValueError("No readable text found in PDF")
    
    return text.strip()
