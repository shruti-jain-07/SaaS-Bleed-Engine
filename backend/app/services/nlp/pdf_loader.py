from pathlib import Path
import fitz  # PyMuPDF
from Backend.App.Core.Logging import logger


class PDFLoaderService:
    @staticmethod
    def extract_text_from_pdf(file_path: Path) -> str:
        """
        Extracts raw text from a digital PDF file using PyMuPDF.
        Includes graceful handling/placeholder for scanned OCR fallback.
        """
        try:
            doc = fitz.open(file_path)
            extracted_text = []

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text("text")
                if text.strip():
                    extracted_text.append(text)

            full_text = "\n".join(extracted_text)

            # OCR Fallback Interface Check
            if not full_text.strip():
                logger.warning(
                    f"No digital text layer found in {file_path.name}. OCR fallback required."
                )
                return "[OCR FALLBACK]: Scanned document detected. Digital text layer unavailable."

            return full_text
        except Exception as e:
            logger.error(f"Error parsing PDF file {file_path}: {str(e)}")
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")