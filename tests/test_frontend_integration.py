import pytest
from backend.app.services.analytics.recommendations import (
    RecommendationEngineService,
)
from backend.app.services.reports.generator import ReportGeneratorService


def test_recommendation_generation():
    assert hasattr(
        RecommendationEngineService, "generate_recommendations"
    )


def test_report_service():
    assert hasattr(ReportGeneratorService, "generate_csv_report")
    assert hasattr(ReportGeneratorService, "generate_pdf_summary")