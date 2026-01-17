Task Management API 

A robust RESTful API built with FastAPI for managing tasks with user authentication, role-based authorization, and comprehensive task management features.


### Features
Authentication

User registration with validation
JWT-based authentication (Access + Refresh tokens)
Password hashing with bcrypt
User profile management
Secure logout

Task Management

Create, read, update, delete tasks
Task filtering by status, priority, and search
Task statistics dashboard
Due date management
Task assignment

Admin Features

User management (view all users)
Role management (user/admin)
Delete users
View all tasks

Security

JWT token authentication
Password strength validation
Rate limiting (100 requests/15 minutes)
CORS configuration
SQL injection prevention
Role-based access control (RBAC)

 Tech Stack

Framework: FastAPI
Database: PostgreSQL with SQLAlchemy ORM
Authentication: JWT (python-jose)
Password Hashing: bcrypt (passlib)
Validation: Pydantic v2
Rate Limiting: SlowAPI

 ### Prerequisites

Python 3.9+
PostgreSQL 12+
pip (Python package manager)

 Installation & Setup
1. Clone the repository
bashgit clone https://github.com/yourusername/task-management-api.git
cd task-management-api
2. Create virtual environment
bashpython -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
3. Install dependencies
bashpip install -r requirements.txt
4. Set up PostgreSQL database
bash# Create database
createdb taskmanagement

# Or using psql
psql -U postgres
CREATE DATABASE taskmanagement;
5. Configure environment variables
bashcp .env.example .env
Edit .env with your configuration:
envDATABASE_URL=postgresql://user:password@localhost:5432/taskmanagement
SECRET_KEY=your-super-secret-key-change-this
6. Run the application
bashuvicorn app.main:app --reload
The API will be available at: http://localhost:8000
### API Documentation
Once the server is running, access:

Swagger UI: http://localhost:8000/api/docs
ReDoc: http://localhost:8000/api/redoc

 API Endpoints
Authentication
POST   /api/v1/auth/register      - Register new user
POST   /api/v1/auth/login         - User login
GET    /api/v1/auth/me            - Get current user
POST   /api/v1/auth/logout        - User logout
POST   /api/v1/auth/refresh       - Refresh access token
Tasks
POST   /api/v1/tasks              - Create task
GET    /api/v1/tasks              - Get all tasks (with filters)
GET    /api/v1/tasks/{id}         - Get single task
PUT    /api/v1/tasks/{id}         - Update task
DELETE /api/v1/tasks/{id}         - Delete task
GET    /api/v1/tasks/statistics   - Get task statistics
Admin
GET    /api/v1/admin/users            - Get all users
PUT    /api/v1/admin/users/{id}/role  - Update user role
DELETE /api/v1/admin/users/{id}       - Delete user
 Usage Examples
Register User
bashcurl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
Login
bashcurl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
Create Task (with token)
bashcurl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project",
    "description": "Finish the task management API",
    "status": "pending",
    "priority": "high",
    "due_date": "2024-12-31T23:59:59"
  }'
Get Tasks with Filters
bashcurl "http://localhost:8000/api/v1/tasks?status=pending&priority=high&search=project" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
 Testing
bash# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
 Security Features

Password Requirements:

Minimum 8 characters
At least one uppercase letter
At least one lowercase letter
At least one number


Token Expiry:

Access token: 15 minutes
Refresh token: 7 days


Rate Limiting: 100 requests per 15 minutes per IP
RBAC Authorization:

Users: Can only see/manage their own tasks
Admins: Can see/manage all tasks and users



📁 Project Structure
task-management-api/
├── app/
│   ├── database/          # Database configuration
│   ├── middleware/        # Auth, authorization, rate limiting
│   ├── models/           # SQLAlchemy models
│   ├── routes/           # API endpoints
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   ├── utils/            # Helper functions
│   ├── config.py         # Settings
│   └── main.py           # Application entry
├── tests/                # Test files
├── .env.example          # Environment template
├── requirements.txt      # Dependencies
└── README.md            # Documentation

### License
This project is licensed under the MIT License.
 Author
Deepanshi verma - deepanshiverma-antino
 Acknowledgments

FastAPI documentation
SQLAlchemy documentation
Python community

