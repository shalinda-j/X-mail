# X-mail

Bulk Email Sender & API

## Requirements

- Python 3.7+
- Django 3.2+
- Django Rest Framework 3.12+
- Celery 5.0+
- Redis 6.0+

## How to Run

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/x-mail.git
   cd x-mail
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```
   cp .env.example .env
   ```
   Edit the `.env` file with your configuration.

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Start the Django development server:
   ```
   python manage.py runserver
   ```

6. In a separate terminal, start Celery worker:
   ```
   celery -A x_mail worker -l info
   ```

7. Access the application at `http://localhost:8000`

For API documentation, visit `http://localhost:8000/api/docs/`
