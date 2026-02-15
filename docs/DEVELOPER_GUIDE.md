# Developer Guide - Expense Tracking System

## 1. Project Overview
This is a **Django-based Expense Tracker** application designed to help users manage personal finances and family expenses. It features a modern, responsive UI built with **Tailwind CSS** and supports **PostgreSQL (Supabase)** for production data storage.

### Technology Stack
*   **Backend:** Django 5.x (Python 3.14+)
*   **Frontend:** HTML5, Tailwind CSS (via CDN or PyTailwindCSS), JavaScript
*   **Database:** PostgreSQL (Production) / SQLite (Local Fallback)
*   **Authentication:** Session-based with PBKDF2 Password Hashing

## 2. Environment Setup

### Prerequisites
*   Python 3.14 or higher
*   pip (Python Package Installer)
*   Git

### Installation Steps
1.  **Clone the Repository**
    ```bash
    git clone https://github.com/anjuraveendran78-source/expense.git
    cd expense
    ```
2.  **Create Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configuration**
    Create a `.env` file in the root directory:
    ```env
    DATABASE_URL=postgresql://[user]:[password]@[host]:6543/postgres
    SECRET_KEY=your-secret-key-here
    DEBUG=True
    ```

5.  **Database Migration**
    ```bash
    python manage.py migrate
    ```

6.  **Run Development Server**
    ```bash
    python manage.py runserver
    ```

## 3. Project Structure
```
expense/
├── expense_tracker/     # Project settings & configuration
│   ├── settings.py      # Main settings (DB, Auth, Apps)
│   ├── urls.py          # Global URL routing
├── user/                # Main application logic
│   ├── models.py        # Database models (User, Transaction, Category)
│   ├── views.py         # Business logic & view controllers
│   ├── urls.py          # App-specific URL routing
│   ├── templates/       # HTML templates (Dashboards, Forms)
├── static/              # Static assets (CSS, JS, Images)
├── requirements.txt     # Python dependencies
└── manage.py            # Django command-line utility
```

## 4. Key Modules

### Authentication (`user/models.py`, `user/views.py`)
*   **Model:** `Registration` (Custom user model).
*   **Hashing:** Passwords are hashed using `django.contrib.auth.hashers.make_password`.
*   **Login:** Verified via `check_password`.

### Transactions
*   **Model:** `Transaction`.
*   **Logic:** Supports both `Income` and `Expense` types.
*   **Family Mode:** Transactions can be linked to the individual user OR the family unit.

### Reporting
*   **Views:** `reports_page` calculates monthly totals and category breakdowns.
*   **Export:** `generate_pdf` uses `xhtml2pdf` to render HTML templates into downloadable PDFs.

## 5. Deployment
The application is configured to automatically detect the `DATABASE_URL` environment variable.
*   **If Present:** Connects to PostgreSQL (Supabase/Heroku/Render).
*   **If Absent:** Falls back to local `db.sqlite3`.

To deploy:
1.  Set `DEBUG=False` in settings.
2.  Configure a production WSGI server (e.g., Gunicorn).
3.  Set up static file serving (e.g., WhiteNoise).
