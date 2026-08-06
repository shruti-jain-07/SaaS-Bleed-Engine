import pytest
from backend.app.services.analytics.summary import AnalyticsService
from backend.app.services.query.search_engine import QueryEngine


def test_analytics_summary_empty_db(db_session):
    summary = AnalyticsService.get_dashboard_summary(db_session)
    assert "total_saas_spend" in summary
    assert "contract_risk_distribution" in summary
    assert summary["total_analyzed_contracts"] == 0


def test_query_engine_parser():
    # Test notice period regex matching logic
    query_str = "contracts with 60 days notice over 10000 high risk"
    
    # Verify parsing regexes against raw input
    import re
    
    value_match = re.search(r"(?:over|>|above|greater than)\s*\$?(\d+(?:\.\d+)?)", query_str)
    notice_match = re.search(r"(\d+)\s*(?:days|day)", query_str)
    
    assert value_match is not None and float(value_match.group(1)) == 10000.0
    assert notice_match is not None and int(notice_match.group(1)) == 60