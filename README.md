# Healthcare Backend API

A comprehensive RESTful API backend system for healthcare management built with Django, Django REST Framework, and PostgreSQL. This system enables secure user authentication, patient management, doctor management, and patient-doctor assignment functionality.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Environment Configuration](#environment-configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
- [Testing with Postman](#testing-with-postman)
- [Error Handling](#error-handling)
- [Security Features](#security-features)
- [Contributing](#contributing)

---

## ✨ Features

- **User Authentication**: Secure JWT-based authentication system
- **Patient Management**: Full CRUD operations for patient records
- **Doctor Management**: Complete doctor profile management
- **Patient-Doctor Mapping**: Assign and manage doctor-patient relationships
- **Data Isolation**: Users can only access their own patient data
- **Input Validation**: Comprehensive validation for all API inputs
- **Error Handling**: Meaningful error messages with proper HTTP status codes
- **Scalable Architecture**: Modular app-based structure for easy maintenance

---

## 🛠️ Tech Stack

- **Backend Framework**: Django 5.2.7
- **API Framework**: Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Language**: Python 3.12+
- **Environment Management**: python-decouple

---

## 📁 Project Structure

```
healthcare_backend/
│
├── healthcare_backend/          # Main project directory
│   ├── __init__.py
│   ├── settings.py             # Project settings
│   ├── urls.py                 # Root URL configuration
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/                        # All Django apps
│   ├── __init__.py
│   │
│   ├── authentication/          # User authentication
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py           # Custom User model
│   │   ├── serializers.py      # Registration/Login serializers
│   │   ├── views.py            # Auth views
│   │   └── urls.py
│   │
│   ├── patients/                # Patient management
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py           # Patient model
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   ├── doctors/                 # Doctor management
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py           # Doctor model
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   └── mappings/                # Patient-Doctor relationships
│       ├── migrations/
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py           # Mapping model
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
│
├── .env                         # Environment variables (not in git)
├── .env.example                 # Environment template
├── .gitignore
├── requirements.txt
├── manage.py
└── README.md
```

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.12 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)
- Virtual environment tool

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd healthcare_backend
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- Django==5.2.7
- djangorestframework
- djangorestframework-simplejwt
- psycopg2-binary
- python-decouple
- django-extensions (optional, for development)

---

## ⚙️ Environment Configuration

### Create `.env` file

Create a `.env` file in the project root directory:

```env
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
DATABASE_NAME=healthcare_db
DATABASE_USER=postgres
DATABASE_PASSWORD=your_postgres_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

**Security Note**: Never commit the `.env` file to version control. Use `.env.example` as a template.

### `.env.example` Template

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

---

## 🗄️ Database Setup

### Step 1: Create PostgreSQL Database

```bash
# Open PostgreSQL command line
psql -U postgres

# Create database
CREATE DATABASE healthcare_db;

# Verify database creation
\l

# Exit psql
\q
```

### Step 2: Run Migrations

```bash
# Create migration files
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate
```

### Step 3: Create Superuser (Admin)

```bash
python manage.py createsuperuser
# Enter email, name, and password when prompted
```

---

## ▶️ Running the Application

### Start Development Server

```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

### Access Admin Panel

Visit `http://127.0.0.1:8000/admin/` and login with superuser credentials.

### API Root Endpoint

Visit `http://127.0.0.1:8000/api/` to see available endpoints.

---

## 📚 API Documentation

### Base URL

```
http://127.0.0.1:8000/api/
```

### Response Format

All API responses follow this structure:

**Success Response:**
```json
{
    "message": "Operation successful",
    "data": { ... }
}
```

**Error Response:**
```json
{
    "error": "Error description",
    "details": { ... }
}
```

---

## 🔐 Authentication

This API uses JWT (JSON Web Token) authentication.

### Registration Flow

1. Register a new user via `/api/auth/register/`
2. Receive user credentials
3. Login via `/api/auth/login/`
4. Receive JWT access and refresh tokens
5. Include access token in all subsequent requests

### Token Usage

Include the access token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

### Token Expiry

- **Access Token**: Valid for 5 hours
- **Refresh Token**: Valid for 1 day

---

## 🔌 API Endpoints

### Authentication APIs (Public - No Auth Required)

#### 1. User Registration
```http
POST /api/auth/register/
Content-Type: application/json

{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!"
}
```

**Response (201 Created):**
```json
{
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com"
    }
}
```

#### 2. User Login
```http
POST /api/auth/login/
Content-Type: application/json

{
    "email": "john@example.com",
    "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
    "message": "Login successful",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
        "id": 1,
        "email": "john@example.com",
        "name": "John Doe"
    }
}
```

---

### Patient APIs (Authentication Required)

#### 1. Create Patient
```http
POST /api/patients/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "name": "Alice Smith",
    "email": "alice@example.com",
    "phone_number": "+1234567890",
    "address": "123 Main St, New York, NY 10001",
    "date_of_birth": "1990-05-15",
    "blood_group": "A+",
    "medical_history": "No known allergies."
}
```

**Response (201 Created):**
```json
{
    "message": "Patient created successfully",
    "patient": {
        "id": 1,
        "name": "Alice Smith",
        "email": "alice@example.com",
        "phone_number": "+1234567890",
        "address": "123 Main St, New York, NY 10001",
        "date_of_birth": "1990-05-15",
        "blood_group": "A+",
        "medical_history": "No known allergies.",
        "created_by": 1,
        "created_by_details": {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "date_joined": "2025-01-05T10:30:00Z"
        },
        "created_at": "2025-01-05T10:35:00Z",
        "updated_at": "2025-01-05T10:35:00Z"
    }
}
```

#### 2. Get All Patients
```http
GET /api/patients/
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "count": 2,
    "patients": [
        {
            "id": 1,
            "name": "Alice Smith",
            "email": "alice@example.com",
            "phone_number": "+1234567890",
            "blood_group": "A+",
            "created_by_name": "John Doe",
            "created_at": "2025-01-05T10:35:00Z"
        }
    ]
}
```

#### 3. Get Single Patient
```http
GET /api/patients/{id}/
Authorization: Bearer <access_token>
```

#### 4. Update Patient (Full Update)
```http
PUT /api/patients/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "name": "Alice Smith",
    "email": "alice@example.com",
    "phone_number": "+1234567890",
    "address": "456 New Address, Brooklyn, NY 11201",
    "date_of_birth": "1990-05-15",
    "blood_group": "A+",
    "medical_history": "Updated medical history."
}
```

#### 5. Update Patient (Partial Update)
```http
PATCH /api/patients/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "address": "789 Updated St, Manhattan, NY 10002"
}
```

#### 6. Delete Patient
```http
DELETE /api/patients/{id}/
Authorization: Bearer <access_token>
```

**Response (204 No Content):**
```json
{
    "message": "Patient deleted successfully"
}
```

---

### Doctor APIs (Authentication Required)

#### 1. Create Doctor
```http
POST /api/doctors/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "name": "Sarah Williams",
    "email": "dr.sarah@hospital.com",
    "phone_number": "+1122334455",
    "specialization": "Cardiologist",
    "qualification": "MBBS, MD (Cardiology)",
    "experience_years": 10,
    "license_number": "MED-2024-001",
    "clinic_address": "City Hospital, 789 Medical Center, NY",
    "consultation_fee": 150.00,
    "is_available": true
}
```

**Response (201 Created):**
```json
{
    "message": "Doctor created successfully",
    "doctor": {
        "id": 1,
        "name": "Sarah Williams",
        "email": "dr.sarah@hospital.com",
        "phone_number": "+1122334455",
        "specialization": "Cardiologist",
        "qualification": "MBBS, MD (Cardiology)",
        "experience_years": 10,
        "license_number": "MED-2024-001",
        "clinic_address": "City Hospital, 789 Medical Center, NY",
        "consultation_fee": "150.00",
        "is_available": true,
        "created_at": "2025-01-05T11:00:00Z",
        "updated_at": "2025-01-05T11:00:00Z"
    }
}
```

#### 2. Get All Doctors
```http
GET /api/doctors/
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "count": 2,
    "doctors": [
        {
            "id": 1,
            "name": "Sarah Williams",
            "specialization": "Cardiologist",
            "experience_years": 10,
            "consultation_fee": "150.00",
            "is_available": true
        }
    ]
}
```

#### 3. Get Single Doctor
```http
GET /api/doctors/{id}/
Authorization: Bearer <access_token>
```

#### 4. Update Doctor
```http
PUT /api/doctors/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "name": "Sarah Williams",
    "email": "dr.sarah@hospital.com",
    "phone_number": "+1122334455",
    "specialization": "Cardiologist",
    "qualification": "MBBS, MD (Cardiology)",
    "experience_years": 12,
    "license_number": "MED-2024-001",
    "clinic_address": "City Hospital, 789 Medical Center, NY",
    "consultation_fee": 200.00,
    "is_available": true
}
```

#### 5. Delete Doctor
```http
DELETE /api/doctors/{id}/
Authorization: Bearer <access_token>
```

---

### Patient-Doctor Mapping APIs (Authentication Required)

#### 1. Assign Doctor to Patient
```http
POST /api/mappings/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "patient": 1,
    "doctor": 1,
    "notes": "Primary cardiologist for routine checkups",
    "is_active": true
}
```

**Response (201 Created):**
```json
{
    "message": "Doctor assigned to patient successfully",
    "mapping": {
        "id": 1,
        "patient": 1,
        "doctor": 1,
        "patient_details": { ... },
        "doctor_details": { ... },
        "assigned_by": 1,
        "assigned_by_name": "John Doe",
        "assigned_date": "2025-01-05T11:15:00Z",
        "notes": "Primary cardiologist for routine checkups",
        "is_active": true
    }
}
```

#### 2. Get All Mappings
```http
GET /api/mappings/
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "count": 2,
    "mappings": [
        {
            "id": 1,
            "patient_name": "Alice Smith",
            "doctor_name": "Sarah Williams",
            "doctor_specialization": "Cardiologist",
            "assigned_date": "2025-01-05T11:15:00Z",
            "is_active": true
        }
    ]
}
```

#### 3. Get All Doctors for a Patient
```http
GET /api/mappings/{patient_id}/
Authorization: Bearer <access_token>
```

**Note:** The ID in the URL is the `patient_id`, not the mapping ID.

**Response (200 OK):**
```json
{
    "patient_id": 1,
    "patient_name": "Alice Smith",
    "total_doctors": 2,
    "doctors": [
        {
            "id": 1,
            "name": "Sarah Williams",
            "email": "dr.sarah@hospital.com",
            "specialization": "Cardiologist",
            "qualification": "MBBS, MD (Cardiology)",
            "experience_years": 10,
            "consultation_fee": "150.00",
            "is_available": true
        }
    ]
}
```

#### 4. Remove Doctor from Patient
```http
DELETE /api/mappings/{id}/
Authorization: Bearer <access_token>
```

**Note:** The ID here is the `mapping_id`.

**Response (204 No Content):**
```json
{
    "message": "Dr. Sarah Williams removed from patient Alice Smith successfully"
}
```

---

## 🧪 Testing with Postman

### Setup Postman Collection

1. **Create a new Collection**: "Healthcare Backend API"
2. **Set Collection Variables**:
   - `base_url`: `http://127.0.0.1:8000/api`
   - `access_token`: (Will be set after login)

### Authentication Flow

1. **Register a User**
   - Save the response

2. **Login**
   - Copy the `access` token from response
   - Set it as a collection variable or environment variable

3. **Configure Authorization**
   - For all protected endpoints:
   - Go to Authorization tab
   - Select Type: "Bearer Token"
   - Token: `{{access_token}}`

### Test Order

1. ✅ Register User
2. ✅ Login User
3. ✅ Create Patient
4. ✅ Get All Patients
5. ✅ Create Doctor
6. ✅ Get All Doctors
7. ✅ Assign Doctor to Patient
8. ✅ Get Doctors for Patient
9. ✅ Update Patient
10. ✅ Delete Mapping
11. ✅ Delete Patient

---

## ⚠️ Error Handling

### Common HTTP Status Codes

- `200 OK`: Successful GET request
- `201 Created`: Successful POST request (resource created)
- `204 No Content`: Successful DELETE request
- `400 Bad Request`: Validation error or malformed request
- `401 Unauthorized`: Authentication required or token invalid
- `403 Forbidden`: User doesn't have permission
- `404 Not Found`: Resource doesn't exist
- `500 Internal Server Error`: Server error

### Error Response Format

```json
{
    "error": "Error description",
    "details": {
        "field_name": [
            "Error message for this field"
        ]
    }
}
```

### Common Errors

#### 1. Unauthorized Access
```json
{
    "detail": "Authentication credentials were not provided."
}
```
**Solution**: Include the JWT token in Authorization header.

#### 2. Token Expired
```json
{
    "detail": "Given token not valid for any token type",
    "code": "token_not_valid"
}
```
**Solution**: Login again to get a new token.

#### 3. Validation Error
```json
{
    "error": "Failed to create patient",
    "details": {
        "email": ["A patient with this email already exists."]
    }
}
```

---

## 🔒 Security Features

### Implemented Security Measures

1. **JWT Authentication**: Secure token-based authentication
2. **Password Hashing**: Passwords are hashed using Django's built-in hashers
3. **Email Validation**: Email format validation
4. **Password Validation**: Strong password requirements
5. **Data Isolation**: Users can only access their own patients
6. **CSRF Protection**: Enabled for non-API views
7. **Environment Variables**: Sensitive data stored in `.env` file

### Best Practices

- Never commit `.env` file to version control
- Change `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Use HTTPS in production
- Implement rate limiting for production
- Regular security updates

---

## 🚀 Deployment Considerations

### Before Deploying to Production

1. **Update Settings**:
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   ```

2. **Static Files**:
   ```bash
   python manage.py collectstatic
   ```

3. **Database**:
   - Use managed PostgreSQL service (AWS RDS, Heroku Postgres, etc.)
   - Enable database backups

4. **Security**:
   - Use strong `SECRET_KEY`
   - Enable HTTPS
   - Configure CORS properly
   - Add rate limiting

5. **Server**:
   - Use production WSGI server (Gunicorn, uWSGI)
   - Configure web server (Nginx, Apache)

---

## 📝 Development Guidelines

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to classes and methods
- Keep functions small and focused

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "Add descriptive commit message"

# Push to remote
git push origin feature/your-feature-name
```

### Adding New Features

1. Create new app if needed: `python manage.py startapp app_name`
2. Define models in `models.py`
3. Create serializers in `serializers.py`
4. Implement views in `views.py`
5. Configure URLs in `urls.py`
6. Write tests
7. Update documentation

---

## 🧪 Running Tests

```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test apps.patients

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 📦 Database Backup and Restore

### Backup Database

```bash
pg_dump -U postgres healthcare_db > backup.sql
```

### Restore Database

```bash
psql -U postgres healthcare_db < backup.sql
```

---

## 🐛 Troubleshooting

### Issue: Module not found

**Solution**: Ensure virtual environment is activated and dependencies are installed.

```bash
pip install -r requirements.txt
```

### Issue: Database connection error

**Solution**: Check PostgreSQL is running and credentials in `.env` are correct.

```bash
# Check PostgreSQL status
# Windows:
Get-Service -Name postgresql*

# Linux/Mac:
sudo systemctl status postgresql
```

### Issue: Migration errors

**Solution**: Delete migration files (except `__init__.py`) and migrate again.

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 📞 Support

For issues, questions, or contributions:

- Create an issue in the repository
- Email: your-tamboliaftab84@gmail.com


---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👥 Contributors

- **Aftab Tamboli**  - [GitHub](https://github.com/Aftab073)

---

## 🙏 Acknowledgments

- Django Documentation
- Django REST Framework Documentation
- PostgreSQL Documentation
- Community contributors

---

## 📈 Version History

- **v1.0.0** (2025-01-05)
  - Initial release
  - User authentication
  - Patient management
  - Doctor management
  - Patient-Doctor mapping

---

**Built with ❤️ using Django and Django REST Framework**