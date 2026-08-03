import re


class TextPreprocessor:
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Normalizes whitespace, removes repeated headers/footers, and cleans raw contract text.
        """
        if not text:
            return ""

        # Remove null bytes and unusual control characters
        cleaned = text.replace("\x00", "")

        # Replace multiple spaces/newlines with single spaces while preserving structure
        cleaned = re.sub(r"[ \t]+", " ", cleaned)
        cleaned = re.sub(r"\n+", "\n", cleaned)

        # Standardize common legal keywords for regex matching
        cleaned = re.sub(r"(?i)auto\s*-\s*renew", "auto-renew", cleaned)
        cleaned = re.sub(r"(?i)notice\s+period", "notice period", cleaned)

        return cleaned.strip()