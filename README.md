# Core E-commerce Project

This is a basic Django e-commerce project scaffold.

## Setup

1. **Create and activate virtual environment**

   ```bash
   cd d:\Django
   py -3 -m venv venv
   venv\Scripts\activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Apply migrations**

   ```bash
   venv\Scripts\python manage.py migrate
   ```

4. **Run development server**

   ```bash
   venv\Scripts\python manage.py runserver
   ```

## Apps

- `core` – main project configuration
- `shop` – e-commerce app (products, cart, orders, etc. to be implemented)

## Static & Media

- Place project-level static files in `static/`.
- User-uploaded media will be stored in `media/` (configured in `core/settings.py`).

