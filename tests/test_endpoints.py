import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# IMPORT the existing model and Base — do not re-declare class ContractAnalysisModel!
from backend.app.db.session import Base, get_db
from backend.app.main import app
from backend.app.models.models import ContractAnalysisModel  # noqa: F401

# Setup in-memory SQLite engine with StaticPool for multi-threaded TestClient
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# Initialize schema once at module load
Base.metadata.create_all(bind=engine)

client = TestClient(app)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_analytics_summary_endpoint():
    response = client.get("/api/v1/analytics/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_saas_spend" in data
    assert "contract_risk_distribution" in data


def test_query_search_endpoint():
    response = client.get("/api/v1/query/search?q=CRITICAL")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_upload_contract_endpoint():
    file_content = b"Contract Agreement with Acme Corp. Annual value $60000. Auto-renewal clause active."
    response = client.post(
        "/api/v1/contracts/upload",
        files={"file": ("test_contract.txt", file_content, "text/plain")},
    )
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["filename"] == "test_contract.txt"
    assert "risk_level" in data
    
def test_query_search_pagination_endpoint():
    response = client.get("/api/v1/query/search?q=CRITICAL&limit=5&offset=0&sort_by=risk_score&sort_order=desc")
    assert response.status_code == 200
    assert isinstance(response.json(), list)