# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MyHub is a Django-based personal productivity system with multiple apps:
- **projects** - Track personal projects with status and metadata
- **tasks** - Task management with deadlines and project associations
- **finance** - Financial tracking with accounts, transactions, and subscriptions
- **learning** - Course/learning progress tracking
- **analytics** - Event tracking and analytics
- **worklogs** - Work feature/completion logging
- **notifications** - SMS reminders via mNotify integration
- **accounts** - User profile and authentication extensions

## Common Commands

### Running the Development Server
```bash
python manage.py runserver
```

### Database Operations
```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create a new app
python manage.py startapp <app_name>
```

### Testing
```bash
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test projects

# Run a specific test class
python manage.py test projects.tests.ProjectModelTests
```

### Celery (Background Tasks)
```bash
# Start Celery worker (run alongside Django server)
celery -A myhub worker -l INFO

# Start Celery Beat scheduler (for periodic tasks)
celery -A myhub beat -l INFO
```

### Static Files (Production)
```bash
python manage.py collectstatic
```

## Architecture Patterns

### Common Mixins (`myhub/mixins.py`)
Views use these shared mixins:
- **UserIsOwnerMixin** - Ensures current user owns the object (checks `user` or `owner` attribute)
- **SuccessMessageMixin** - Adds success messages for CRUD operations
- **FilterMixin** - Provides common filtering/search for ListViews
- **CSVExportMixin** - Adds CSV export via `?format=csv` query param

### View Pattern
Class-based views follow this pattern:
- All views use `LoginRequiredMixin`
- Detail/Update/Delete views use `UserIsOwnerMixin`
- Create/Update/Delete views use `SuccessMessageMixin`
- ListViews support search and filtering via query params

### Model Patterns
- Models use `owner` or `user` ForeignKey to `settings.AUTH_USER_MODEL`
- Use `select_related()` and `prefetch_related()` for query optimization
- Define `get_absolute_url()` for canonical URLs

## Database Configuration

The project uses PostgreSQL in production via `DATABASE_URL` environment variable. Falls back to SQLite for local development. Database config is in `myhub/settings.py` using `dj_database_url`.

## Celery Integration

- Configuration in `myhub/settings.py` and `myhub/celery.py`
- Redis is the default broker/backend
- Periodic tasks are scheduled via `CELERY_BEAT_SCHEDULE`
- Uses `django_celery_beat` for database-stored schedules
- Scheduled: `notifications.send_all_reminders` every 15 minutes

## SMS Notifications (mNotify)

SMS service is in `notifications/services/mnotify.py`. Environment variables:
- `MNOTIFY_API_KEY`
- `MNOTIFY_SENDER_ID`
- `MNOTIFY_SMS_URL`

## PWA Features

The app is a Progressive Web App with:
- Service worker at `static/sw.js`
- Manifest at `static/manifest.json`
- Offline support with offline page at `templates/offline.html`
- Requires HTTPS for service worker (localhost is exception)
- Icon generation via `generate_icons.py`

## Project Structure

```
myhub/           # Main project settings, URLs, Celery config
templates/       # Global templates (base.html, dashboard.html, offline.html)
static/          # Static files (CSS, JS, icons, manifest.json)
<app>/           # Individual Django apps
  ├── models.py
  ├── views.py
  ├── forms.py
  ├── urls.py
  └── tests.py
```

## Environment Variables

Key variables (typically in `.env`):
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)
- `ALLOWED_HOSTS` - Comma-separated list
- `CELERY_BROKER_URL` - Redis URL
- `MNOTIFY_API_KEY` - SMS API key
- `SUBSCRIPTION_REMINDER_DAYS_BEFORE` - Days before subscription to remind (default: 2)
- `TASK_REMINDER_MINUTES_BEFORE` - Minutes before task deadline to remind (default: 120)
