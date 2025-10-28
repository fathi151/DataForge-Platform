# Data Platform API Backend

REST API backend for the Data Platform dashboard, providing endpoints for data retrieval and platform monitoring.

## 🎯 Features

- **Dashboard API**: Real-time platform statistics
- **Data Quality API**: Data quality metrics and monitoring
- **Pipeline API**: Pipeline status and execution tracking
- **Services API**: Service health and system monitoring
- **Analytics API**: Business metrics and analytics
- **CORS Support**: Cross-origin requests enabled
- **Health Checks**: Built-in health check endpoint

## 🛠️ Technology Stack

- **Flask**: Lightweight Python web framework
- **PostgreSQL**: Database connection
- **Gunicorn**: Production WSGI server
- **Flask-CORS**: Cross-origin resource sharing

## 📦 Installation

### Prerequisites

- Python 3.11+
- PostgreSQL
- Docker (optional)

### Local Development

1. Navigate to the API directory:
```bash
cd api
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables:
```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=datawarehouse
export DB_USER=datauser
export DB_PASSWORD=datapass123
```

5. Run the development server:
```bash
python app.py
```

The API will be available at `http://localhost:8000`

### Docker Build

Build the Docker image:
```bash
docker build -t data-platform-api:latest .
```

Run the container:
```bash
docker run -p 8000:8000 \
  -e DB_HOST=postgres \
  -e DB_USER=datauser \
  -e DB_PASSWORD=datapass123 \
  data-platform-api:latest
```

## 📚 API Endpoints

### Health Check

```
GET /health
```

Returns the API health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-06T10:30:00"
}
```

### Dashboard

#### Get Dashboard Statistics
```
GET /api/dashboard/stats
```

Returns key platform statistics and metrics.

**Response:**
```json
{
  "totalRecords": 125430,
  "activeUsers": 1234,
  "pipelineSuccess": 98.5,
  "avgResponseTime": 245,
  "dailySales": [
    {
      "date": "2024-01-01",
      "orders": 120,
      "sales": 4200
    }
  ]
}
```

### Data Quality

#### Get Data Quality Metrics
```
GET /api/data-quality/metrics
```

Returns data quality scores and metrics.

**Response:**
```json
{
  "overallScore": 98.5,
  "validRecords": 125000,
  "invalidRecords": 430,
  "tableQuality": [
    {
      "table_name": "customers",
      "total_records": 5000,
      "valid_records": 4950
    }
  ]
}
```

### Pipelines

#### Get Pipeline Status
```
GET /api/pipelines/status
```

Returns status of all ETL pipelines.

**Response:**
```json
[
  {
    "id": 1,
    "name": "ETL Pipeline",
    "status": "running",
    "progress": 65,
    "lastRun": "2024-01-06T02:00:00",
    "nextRun": "2024-01-07T02:00:00"
  }
]
```

### Services

#### Get Services Status
```
GET /api/services/status
```

Returns status of all platform services.

**Response:**
```json
[
  {
    "name": "PostgreSQL",
    "status": "running",
    "port": 5432
  }
]
```

#### Get System Statistics
```
GET /api/services/system-stats
```

Returns system resource usage statistics.

**Response:**
```json
{
  "cpuUsage": 45,
  "memoryUsage": 62,
  "diskUsage": 38,
  "networkLatency": 12
}
```

### Analytics

#### Get Revenue Analytics
```
GET /api/analytics/revenue
```

Returns revenue metrics and trends.

**Response:**
```json
{
  "totalRevenue": 125430,
  "totalOrders": 3240,
  "avgOrderValue": 38.7,
  "conversionRate": 3.2,
  "revenueTrend": [
    {
      "date": "2024-01-01",
      "orders": 120,
      "revenue": 4200
    }
  ]
}
```

#### Get Customer Analytics
```
GET /api/analytics/customers
```

Returns customer metrics and segmentation.

**Response:**
```json
{
  "totalCustomers": 5000,
  "customersByCountry": [
    {
      "country": "USA",
      "count": 2500
    }
  ]
}
```

## 🔧 Configuration

### Environment Variables

```env
# Database Configuration
DB_HOST=postgres
DB_PORT=5432
DB_NAME=datawarehouse
DB_USER=datauser
DB_PASSWORD=datapass123

# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
```

### Database Connection

The API connects to PostgreSQL using the following configuration:

```python
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'postgres'),
    'port': os.getenv('DB_PORT', 5432),
    'database': os.getenv('DB_NAME', 'datawarehouse'),
    'user': os.getenv('DB_USER', 'datauser'),
    'password': os.getenv('DB_PASSWORD', 'datapass123')
}
```

## 🚀 Deployment

### Docker Compose

The API is included in the main `docker-compose.yml`:

```bash
docker-compose up -d api
```

### Production Deployment

For production deployment:

1. Use environment-specific configuration
2. Enable HTTPS/SSL
3. Set up proper logging and monitoring
4. Configure database connection pooling
5. Use a production WSGI server (Gunicorn)

## 📊 Database Queries

The API uses the following database schema:

### Raw Data Layer
- `raw_data.customers` - Customer information
- `raw_data.orders` - Order data
- `raw_data.products` - Product catalog
- `raw_data.order_items` - Order line items

### Analytics Layer
- `analytics.customer_metrics` - Customer KPIs
- `analytics.daily_sales` - Daily sales aggregates

## 🔍 Monitoring

### Health Check

Monitor API health:
```bash
curl http://localhost:8000/health
```

### Logging

Logs are output to console and can be captured by Docker:
```bash
docker logs data-platform-api
```

## 🐛 Troubleshooting

### Database Connection Error

Ensure PostgreSQL is running and accessible:
```bash
psql -h localhost -U datauser -d datawarehouse
```

### Port Already in Use

Change the port in the Dockerfile or docker-compose.yml:
```bash
docker run -p 8001:8000 data-platform-api:latest
```

### Import Errors

Reinstall dependencies:
```bash
pip install --force-reinstall -r requirements.txt
```

## 📖 Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Gunicorn Documentation](https://gunicorn.org/)
- [Flask-CORS Documentation](https://flask-cors.readthedocs.io/)

## 📝 License

This project is part of the Data Platform demonstrator.

## 🤝 Contributing

To contribute improvements:

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

---

**Last Updated**: 2024
**Version**: 1.0.0
