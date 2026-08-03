# API Specification - Sprint 1 Ingestion Services

## Endpoints

### 1. Health Check
* **URL:** `/health`
* **Method:** `GET`
* **Response:** `200 OK`
```json
{
  "status": "healthy",
  "service": "SaaS Bleed Engine"
}