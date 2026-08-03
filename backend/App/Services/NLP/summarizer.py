from typing import Dict, Any


class ContractSummarizer:
    @staticmethod
    def generate_summary(
        entities: Dict[str, Any], risk_analysis: Dict[str, Any]
    ) -> str:
        """
        Generates a structured executive summary highlighting contract obligations and risks.
        """
        vendor = entities.get("vendor_name", "Vendor")
        val = entities.get("contract_value", 0.0)
        notice = entities.get("notice_period_days", 30)
        level = risk_analysis.get("risk_level", "MEDIUM")

        summary = (
            f"EXECUTIVE SUMMARY: Agreement with {vendor} valued at ${val:,.2f}. "
            f"Contract carries a {level} risk profile. "
            f"Key Requirement: Requires a {notice}-day written cancellation notice period prior to renewal."
        )
        return summary