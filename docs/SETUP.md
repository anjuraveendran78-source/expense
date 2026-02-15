# Project Setup & Installation

## Prerequisites
- Python 3.14+
- `pip`
- A Supabase account (for PostgreSQL database)

## Local Development Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/your-repo/expense-tracker.git
    cd expense-tracker
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Variables**
    Create a `.env` file in the root directory:
    ```env
    DATABASE_URL="postgresql://postgres:[YOUR-PASSWORD]@[YOUR-HOST]:6543/postgres"
    SECRET_KEY="your-django-secret-key"
    DEBUG=True
    ```
    *Note: For Supabase Transaction Pooler (port 6543), ensure your URL ends with `?sslmode=require` or is handled by `dj_database_url` (which we verified it is).*

5.  **Database Migration**
    Apply migrations to create tables in Supabase:
    ```bash
    python manage.py migrate
    ```

6.  **Create Superuser (Optional)**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the Server**
    ```bash
    python manage.py runserver
    ```
    Access the app at `http://127.0.0.1:8000`.

## Production Deployment

- Ensure `DEBUG=False` in production.
- Use a WSGI server like `gunicorn`.
- Set up static files serving (e.g., WhiteNoise).

## Security Note
- Passwords are **hashed** using PBKDF2 (SHA256).
- **Do not commit `.env`** to version control.
