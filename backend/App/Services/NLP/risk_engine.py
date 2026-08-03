from typing import Dict, Any


class ContractRiskEngine:
    @staticmethod
    def evaluate_risk(entities: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assigns a risk level (LOW, MEDIUM, HIGH, CRITICAL) based on auto-renewal clauses and notice windows.
        """
        score = 0
        reasons = []

        auto_renew = entities.get("auto_renew", False)
        notice_days = entities.get("notice_period_days", 30)
        value = entities.get("contract_value", 0.0)

        if auto_renew:
            score += 40
            reasons.append("Contains restrictive auto-renewal clause.")

        if notice_days >= 60:
            score += 30
            reasons.append(
                f"Long cancellation notice period required ({notice_days} days)."
            )

        if value > 50000:
            score += 20
            reasons.append(f"High annual contract value (${value:,.2f}).")

        # Categorize Risk Level
        if score >= 70:
            level = "CRITICAL"
        elif score >= 50:
            level = "HIGH"
        elif score >= 30:
            level = "MEDIUM"
        else:
            level = "LOW"

        return {
            "risk_score": score,
            "risk_level": level,
            "risk_factors": reasons,
        }