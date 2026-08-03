import re
from typing import Dict, Any


class EntityExtractor:
    @staticmethod
    def extract_entities(text: str) -> Dict[str, Any]:
        """
        Extracts key legal and financial entities from clean contract text.
        """
        entities = {
            "vendor_name": EntityExtractor._extract_vendor(text),
            "contract_value": EntityExtractor._extract_value(text),
            "notice_period_days": EntityExtractor._extract_notice_period(text),
            "auto_renew": bool(
                re.search(
                    r"(?i)(auto-renew|automatic renewal|renew automatically)",
                    text,
                )
            ),
            "governing_law": EntityExtractor._extract_governing_law(text),
        }
        return entities

    @staticmethod
    def _extract_vendor(text: str) -> str:
        # Match pattern: "Agreement between Company and [Vendor]"
        match = re.search(
            r"(?i)(?:between|with)\s+([A-Z][A-Za-z0-9\s,\.]+?)(?=\s+(?:and|is|located|\n))",
            text,
        )
        return match.group(1).strip() if match else "Unknown Vendor"

    @staticmethod
    def _extract_value(text: str) -> float:
        # Match dollar amounts: $20,000 or $20000.00
        matches = re.findall(
            r"\$\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})?)", text
        )
        if matches:
            values = [float(m.replace(",", "")) for m in matches]
            return max(values)
        return 0.0

    @staticmethod
    def _extract_notice_period(text: str) -> int:
        # Match: "30 days written notice" or "cancellation notice of 60 days"
        match = re.search(
            r"(?i)(\d+)\s*days?\s+(?:prior\s+)?(?:written\s+)?notice", text
        )
        return int(match.group(1)) if match else 30  # Fallback: 30 days

    @staticmethod
    def _extract_governing_law(text: str) -> str:
        match = re.search(
            r"(?i)governed\s+by\s+the\s+laws\s+of\s+([A-Za-z\s]+)(?=\.|\n)",
            text,
        )
        return match.group(1).strip() if match else "Unspecified"