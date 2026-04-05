# Finance Data Processing and Access Control Backend

## Tech Stack
- Python + Django
- Django REST Framework
- SQLite Database
- JWT Authentication

## Setup Instructions

1. Install dependencies
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers

2. Run migrations
python manage.py migrate

3. Create superuser
python manage.py createsuperuser

4. Run server
python manage.py runserver

## API Endpoints

| Method | URL | Description | Access |
|--------|-----|-------------|--------|
| POST | /api/register/ | Register user | Public |
| POST | /api/login/ | Login & get token | Public |
| GET | /api/users/ | List all users | Admin only |
| GET | /api/transactions/ | List transactions | All roles |
| POST | /api/transactions/ | Create transaction | Analyst, Admin |
| PUT | /api/transactions/<id>/ | Update transaction | Analyst, Admin |
| DELETE | /api/transactions/<id>/ | Delete transaction | Admin only |
| GET | /api/dashboard/ | Summary data | All roles |

## Roles
- Admin - Full access
- Analyst - View + Create + Update
- Viewer - View only

## Database
SQLite used for simplicity and portability.

## Assumptions
- JWT Token required for all APIs except register and login
- Admin panel available at /admin/