# test-service

Just another test

## 🚀 Quick Start

### Development Setup

1. **Clone and install dependencies:**
   ```bash
   git clone https://github.com/casanovg/test-service.git
   cd test-service
   python -m pip install -r requirements.txt
   ```

2. **Start development environment:**
   ```bash
   docker-compose up -d postgres
   uvicorn app.main:app --reload --host 0.0.0.0 --port 5005
   ```

3. **Access the API:**
   - API: http://localhost:5005/api/
   - Docs: http://localhost:5005/docs
   - Health: http://localhost:5005/health

### Production Deployment

The service is automatically deployed via GitHub Actions to:
- **Staging**: http://w1-stg/api/test-service/
- **Production**: http://w1-prd/api/test-service/

## 📁 Project Structure

```
test-service/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── config.py        # Configuration settings
│   ├── database.py      # Database connection
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   └── routes.py        # API routes
├── .github/workflows/   # CI/CD pipeline
├── Dockerfile          # Container definition
├── docker-compose.yml  # Local development
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🗄️ Database

- **Schema**: `test_service`
- **Port**: `5005`
- **Development**: PostgreSQL via docker-compose
- **Production**: Shared PostgreSQL instance

## 🔧 Configuration

Copy `.env.example` to `.env` and adjust settings:

```bash
cp .env.example .env
```

## 📊 Monitoring

- **Health Check**: `GET /health`
- **Metrics**: `GET /metrics`
- **OpenAPI**: `GET /docs`

## 🧪 Testing

```bash
python -m pytest tests/ -v
```

## 📝 API Documentation

Visit `/docs` endpoint for interactive API documentation.

