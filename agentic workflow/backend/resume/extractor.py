"""
PDF Text Extractor
Extracts raw text from PDF resume files
"""
import io
from typing import Union
import pdfplumber


def extract_pdf_text(pdf_file: Union[str, io.BytesIO]) -> str:
    """
    Extract raw text from a PDF file.
    
    Args:
        pdf_file: Either a file path string or a BytesIO object
        
    Returns:
        Extracted text from all pages
    """
    text_parts = []
    
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")
    
    if not text_parts:
        raise ValueError("No text could be extracted from the PDF")
    
    return "\n\n".join(text_parts)


def extract_pdf_from_bytes(pdf_bytes: bytes) -> str:
    """
    Extract text from PDF bytes (for file uploads).
    
    Args:
        pdf_bytes: Raw PDF file bytes
        
    Returns:
        Extracted text
    """
    pdf_io = io.BytesIO(pdf_bytes)
    return extract_pdf_text(pdf_io)


def clean_extracted_text(text: str) -> str:
    """
    Clean up extracted text for better parsing.
    
    Args:
        text: Raw extracted text
        
    Returns:
        Cleaned text
    """
    # Remove excessive whitespace
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Strip whitespace
        line = line.strip()
        # Skip empty lines that are too frequent
        if line or (cleaned_lines and cleaned_lines[-1]):
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)
