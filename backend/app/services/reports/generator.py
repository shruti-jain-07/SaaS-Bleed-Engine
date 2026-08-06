from pathlib import Path
from typing import Any, Dict, List
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


class ReportGeneratorService:

    @staticmethod
    def generate_csv_report(
        data: List[Dict[str, Any]], output_path: Path
    ) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame(data)
        df.to_csv(output_path, index=False)
        return output_path

    @staticmethod
    def generate_pdf_summary(
        recommendations: List[Dict[str, Any]], output_path: Path
    ) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        doc = SimpleDocTemplate(str(output_path), pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Title
        story.append(
            Paragraph(
                "FinOps Executive Spend & Recommendation Report",
                styles["Title"],
            )
        )
        story.append(Spacer(1, 18))

        # Table Data
        table_data = [["Category", "Severity", "Title", "Est. Savings"]]
        for rec in recommendations:
            table_data.append([
                rec.get("category", "General"),
                rec.get("severity", "LOW"),
                rec.get("title", "")[:40],
                f"${rec.get('potential_savings', 0.0):,.2f}",
            ])

        t = Table(table_data, colWidths=[100, 70, 240, 90])
        t.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f77b4")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ])
        )

        story.append(t)
        doc.build(story)
        return output_path