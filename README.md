# Django CMS API

## Overview
This project is a Content Management System (CMS) backend implemented using Django Rest Framework (DRF). It provides a robust API for managing content and supports two distinct user roles: **Admin** and **Author**.

### Key Highlights:
- Token-based authentication using JWT.
- Role-based access control:
  - **Admin**: Full control over all content.
  - **Author**: Manage only their own content.
- Supports CRUD operations for content.
- Search and pagination for content management.

---

## Features
- **User Management**:
  - Author registration.
  - Login using email and password.
  - Token-based authentication with JWT.

- **Content Management**:
  - Create, update, retrieve, and delete content.
  - Support for PDF file uploads.

- **Search and Pagination**:
  - Search content by matching terms in `title`, `body`, `summary`, and `categories`.
  - Paginate results to improve performance and usability.

- **Admin Functionality**:
  - Manage all content.
  - Seed a default admin user.

---

## Installation

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.8+
- pip (Python package installer)
- Git
- Virtualenv (optional but recommended)

### Steps to Install
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/rmhatre404/django_cms.git
   cd django_cms
   ```

2. **Set Up a Virtual Environment** (Optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate   # For Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**:
   - Apply migrations to initialize the database schema:
     ```bash
     python manage.py migrate
     ```

5. **Create a Superuser** (Optional):
   If you want to create an admin manually:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```
   The server will start at: `http://127.0.0.1:8000`

---

## API Documentation
For detailed API instructions, refer to the accompanying PDF document included in the repository. It provides endpoint details, request/response formats, and usage examples.

---

## Default Admin Seeding
To create a default admin user, run the following command:
```bash
python manage.py seed_admin
```
### Default Admin Credentials:
- **Email**: `admin@arcitech.com`
- **Password**: `Admin@123`

---

## Project Structure
```
project_root/
├── cms_project/         # Main project directory
│   ├── settings.py   # Django settings
│   └── urls.py       # Root URL configurations
├── users/              # User management app
│   ├── models.py    # User models
│   ├── views.py     # User-related views
│   └── urls.py      # User-related URL configurations
├── content/            # Content management app
│   ├── models.py    # Content models
│   ├── views.py     # Content-related views
│   └── urls.py      # Content-related URL configurations
└── manage.py           # Django management commands
```

---

## Testing
Unit tests are included for critical functionalities.

### Running Tests:
1. Run all tests:
   ```bash
   python manage.py test
   ```

2. Test coverage can be generated using the `coverage` tool:
   ```bash
   coverage run manage.py test
   coverage html  # Generates an HTML report
   ```

---

## Deployment
To deploy this project, follow these steps:

1. **Production Settings**:
   - Update the `settings.py` file with production configurations (e.g., `ALLOWED_HOSTS`, `DATABASES`).

2. **Collect Static Files**:
   ```bash
   python manage.py collectstatic
   ```

3. **Deploy to a Hosting Service**:
   - Use services like Heroku, AWS, or Render to deploy the application.

---

## Contributing
Contributions are welcome! Feel free to submit a pull request or open an issue for suggestions and bug fixes.

---


