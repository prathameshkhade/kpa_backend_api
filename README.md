# KPA Backend - Wheel Specifications Management API

A Django REST Framework API for managing KPA wheel specification forms with filtering capabilities and comprehensive documentation.

## 🚀 Tech Stack

- **Backend Framework**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL 15
- **API Documentation**: Swagger/OpenAPI (drf-spectacular)
- **Environment Management**: python-dotenv
- **Containerization**: Docker with custom Dockerfile
- **Filtering**: django-filter for advanced query filtering

## 📋 Implemented APIs

### Wheel Specifications API

**POST** `/api/forms/wheel-specifications/`
- Create new wheel specification forms
- Validates form number format (must start with 'WHEEL-')
- Stores technical specifications and metadata
- Returns structured success/error responses

**GET** `/api/forms/wheel-specifications/`
- Retrieve wheel specifications with filtering
- Supports filtering by: `formNumber`, `submittedBy`, `submittedDate`
- Returns paginated results with structured response format

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.12+
- PostgreSQL 15+
- Docker (optional, for containerized deployment)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd kpa_backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   ```
   
   **⚠️ Important**: Edit the `.env` file with your actual configuration values:
   ```env
   SECRET_KEY=your-secret-key-here  # Generate a new Django secret key
   DEBUG=True
   DB_NAME=kpa_db
   DB_USER=postgres
   DB_PASSWORD=your-actual-password  # Use your PostgreSQL password
   DB_HOST=localhost
   DB_PORT=5432
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```
   
   **🔐 Security Note**: Never commit your `.env` file to version control. It contains sensitive information.

5. **Database Setup**
   ```bash
   # Create PostgreSQL database
   createdb kpa_db
   
   # Or using PostgreSQL command line:
   psql -U postgres
   CREATE DATABASE kpa_db;
   \q
   ```

6. **Run Django migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

   The API will be available at: `http://localhost:8000`

### Docker Setup

1. **Build Docker image**
   ```bash
   docker build -t kpa-backend .
   ```

2. **Set up PostgreSQL database**
   
   **Option A: Using local PostgreSQL**
   - Ensure PostgreSQL is running on your host machine
   - Create database as shown in local setup
   
   **Option B: Using Docker PostgreSQL**
   ```bash
   # Run PostgreSQL container
   docker run --name kpa-postgres -d \
     -e POSTGRES_DB=kpa_db \
     -e POSTGRES_USER=postgres \
     -e POSTGRES_PASSWORD=your-password \
     -p 5432:5432 \
     postgres:15-alpine
   ```

3. **Create environment file for Docker**
   ```bash
   # Create .env.docker
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   DB_NAME=kpa_db
   DB_USER=postgres
   DB_PASSWORD=your-password
   DB_HOST=host.docker.internal  # For local PostgreSQL
   # DB_HOST=kpa-postgres        # If using Docker PostgreSQL
   DB_PORT=5432
   ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
   ```

4. **Run Django application container**
   ```bash
   # For local PostgreSQL
   docker run -d --name kpa-backend \
     -p 8000:8000 \
     --env-file .env.docker \
     kpa-backend
   
   # For Docker PostgreSQL (link containers)
   docker run -d --name kpa-backend \
     -p 8000:8000 \
     --env-file .env.docker \
     --link kpa-postgres:postgres \
     kpa-backend
   ```

5. **Run migrations in container**
   ```bash
   docker exec kpa-backend python manage.py migrate
   ```

6. **Create superuser in container (optional)**
   ```bash
   docker exec -it kpa-backend python manage.py createsuperuser
   ```

### Docker Network Setup (Recommended)

For better container communication, use Docker networks:

```bash
# Create network
docker network create kpa-network

# Run PostgreSQL
docker run --name kpa-postgres -d \
  --network kpa-network \
  -e POSTGRES_DB=kpa_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=your-password \
  -p 5432:5432 \
  postgres:15-alpine

# Update .env.docker with:
# DB_HOST=kpa-postgres

# Run Django app
docker run -d --name kpa-backend \
  --network kpa-network \
  -p 8000:8000 \
  --env-file .env.docker \
  kpa-backend
```

## 📚 API Documentation

Access comprehensive API documentation:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/
- **Health Check**: http://localhost:8000/health/

## 🧪 API Testing

### Create Wheel Specification

**Request:**
```bash
curl -X POST http://localhost:8000/api/forms/wheel-specifications/ \
  -H "Content-Type: application/json" \
  -d '{
    "formNumber": "WHEEL-2025-001",
    "submittedBy": "user_id_123",
    "submittedDate": "2025-07-27",
    "fields": {
      "treadDiameterNew": "915 (900-1000)",
      "lastShopIssueSize": "837 (800-900)",
      "condemningDia": "825 (800-900)",
      "wheelGauge": "1600 (+2,-1)",
      "variationSameAxle": "0.5",
      "variationSameBogie": "5",
      "variationSameCoach": "13",
      "wheelProfile": "29.4 Flange Thickness",
      "intermediateWWP": "20 TO 28",
      "bearingSeatDiameter": "130.043 TO 130.068",
      "rollerBearingOuterDia": "280 (+0.0/-0.035)",
      "rollerBearingBoreDia": "130 (+0.0/-0.025)",
      "rollerBearingWidth": "93 (+0/-0.250)",
      "axleBoxHousingBoreDia": "280 (+0.030/+0.052)",
      "wheelDiscWidth": "127 (+4/-0)"
    }
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Wheel specification submitted successfully.",
  "data": {
    "formNumber": "WHEEL-2025-001",
    "submittedBy": "user_id_123",
    "submittedDate": "2025-07-27",
    "status": "Saved"
  }
}
```

### Get Wheel Specifications with Filters

```bash
# Get all wheel specifications
curl http://localhost:8000/api/forms/wheel-specifications/

# Filter by form number
curl "http://localhost:8000/api/forms/wheel-specifications/?formNumber=WHEEL-2025-001"

# Filter by submitted by
curl "http://localhost:8000/api/forms/wheel-specifications/?submittedBy=user_id_123"

# Filter by date
curl "http://localhost:8000/api/forms/wheel-specifications/?submittedDate=2025-07-27"

# Multiple filters
curl "http://localhost:8000/api/forms/wheel-specifications/?formNumber=WHEEL-2025-001&submittedBy=user_id_123"
```

## 🏗️ Project Structure

```
kpa_backend/
├── manage.py
├── requirements.txt
├── Dockerfile
├── .env.example
├── .gitignore
├── README.md
├── kpa_backend/              # Main project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── apps/
    └── forms/                # Forms management app
        ├── __init__.py
        ├── models.py         # WheelSpecification model
        ├── serializers.py    # DRF serializers
        ├── views.py          # API views
        ├── urls.py           # URL routing
        ├── admin.py          # Django admin
        └── migrations/       # Database migrations
```

## 🔒 Security Features

- Environment-based configuration
- Input validation and serialization
- SQL injection prevention (Django ORM)
- Form number validation
- Error handling with structured responses
- CORS protection capabilities

## 📊 Database Schema

### WheelSpecification Model

**Metadata Fields:**
- `form_number` (CharField) - Unique form identifier
- `submitted_by` (CharField) - User who submitted the form
- `submitted_date` (DateField) - Form submission date
- `status` (CharField) - Form status (default: "Saved")
- `created_at` (DateTimeField) - Auto-generated creation timestamp
- `updated_at` (DateTimeField) - Auto-generated update timestamp

**Technical Specification Fields:**
- `tread_diameter_new` - New tread diameter specifications
- `last_shop_issue_size` - Last shop issue size
- `condemning_dia` - Condemning diameter
- `wheel_gauge` - Wheel gauge measurements
- `variation_same_axle` - Variation on same axle
- `variation_same_bogie` - Variation on same bogie
- `variation_same_coach` - Variation on same coach
- `wheel_profile` - Wheel profile specifications
- `intermediate_wwp` - Intermediate WWP measurements
- `bearing_seat_diameter` - Bearing seat diameter
- `roller_bearing_outer_dia` - Roller bearing outer diameter
- `roller_bearing_bore_dia` - Roller bearing bore diameter
- `roller_bearing_width` - Roller bearing width
- `axle_box_housing_bore_dia` - Axle box housing bore diameter
- `wheel_disc_width` - Wheel disc width

## ⚡ API Features

### Response Format
All API responses follow a consistent structure:

**Success Response:**
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": { /* response data */ }
}
```

**Error Response:**
```json
{
  "success": false,
  "message": "Error description",
  "errors": { /* validation errors */ }
}
```

### Filtering Capabilities
- **Form Number**: Exact match filtering
- **Submitted By**: Exact match filtering  
- **Submitted Date**: Date-based filtering (YYYY-MM-DD format)
- **Multiple Filters**: Combine multiple filters using query parameters

### Validation Rules
- Form numbers must start with 'WHEEL-'
- All required fields must be provided
- Date fields must be in valid format
- Field length restrictions as per model definition

## 🌍 Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Django secret key | - | ✅ |
| `DEBUG` | Debug mode | `False` | - |
| `DB_NAME` | Database name | `kpa_db` | ✅ |
| `DB_USER` | Database user | `postgres` | ✅ |
| `DB_PASSWORD` | Database password | - | ✅ |
| `DB_HOST` | Database host | `localhost` | ✅ |
| `DB_PORT` | Database port | `5432` | - |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost` | - |

## 🚀 Production Deployment

### Pre-deployment Checklist:
1. Set `DEBUG=False` in environment
2. Configure proper `SECRET_KEY`
3. Set up production PostgreSQL database
4. Configure `ALLOWED_HOSTS` for your domain
5. Set up reverse proxy (Nginx recommended)
6. Enable SSL/TLS certificates
7. Configure logging and monitoring

### Docker Production Deployment:
```bash
# Build production image
docker build -t kpa-backend:production .

# Run with production environment
docker run -d --name kpa-backend-prod \
  -p 8000:8000 \
  --env-file .env.production \
  --restart unless-stopped \
  kpa-backend:production
```

## 📝 Management Commands

### Database Operations:
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Check for issues
python manage.py check

# Collect static files (if needed)
python manage.py collectstatic
```

### Docker Operations:
```bash
# View container logs
docker logs kpa-backend

# Execute commands in container
docker exec kpa-backend python manage.py migrate

# Stop and remove containers
docker stop kpa-backend
docker rm kpa-backend

# Remove image
docker rmi kpa-backend
```

## 🐛 Troubleshooting

### Common Issues:

**Database Connection Error:**
- Verify PostgreSQL is running
- Check database credentials in `.env`
- Ensure database exists

**Import Error for Exception Handler:**
- The project includes a reference to `apps.common.exceptions` which isn't implemented
- This can be safely removed from settings if not needed

**Docker Container Won't Start:**
- Check environment variables
- Verify database connectivity
- Review container logs: `docker logs kpa-backend`

**API Returns 405 Method Not Allowed:**
- Verify URL routing in `apps/forms/urls.py`
- Check HTTP method (GET/POST) matches endpoint

## 📞 Support

For questions or issues:
- Check the API documentation at `/api/docs/`
- Review the troubleshooting section above
- Examine application logs for detailed error messages

## 📄 License

This project is developed for the KPA assignment evaluation.

---

**Note**: This implementation demonstrates Django REST Framework best practices including proper serialization, validation, error handling, filtering capabilities, and comprehensive API documentation. The Docker setup provides flexibility for both development and production deployments.