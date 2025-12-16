# PostgreSQL Migration Guide

## Overview

This guide will help you migrate your MyHub application from SQLite3 to PostgreSQL.

**Database Details:**
- Host: `157.173.118.68`
- Port: `5432`
- Database: `myhub_db`
- User: `kennedy`

## What's Been Done ✅

1. **Environment Configuration**
   - Created `.env` file with PostgreSQL connection string
   - Updated `settings.py` to use `DATABASE_URL` from environment
   - Added `dj-database-url` support for database URL parsing

2. **Migration Script**
   - Created `migrate_to_postgresql.py` for easy migration
   - Supports export, import, and connection verification

## Migration Steps

### Step 1: Install Required Packages

```bash
pip install psycopg2-binary dj-database-url
```

**Note:**
- `psycopg2-binary` is the PostgreSQL adapter for Django
- `dj-database-url` allows using database connection URLs
- If you encounter build issues with psycopg2, use `psycopg2-binary` instead

### Step 2: Verify PostgreSQL Connection

Test that you can connect to the PostgreSQL database:

```bash
python migrate_to_postgresql.py verify
```

This will:
- Check connection to PostgreSQL server
- Display database version and info
- Show number of existing tables

### Step 3: Export Data from SQLite3

While still using SQLite3, export all your data:

```bash
python migrate_to_postgresql.py export
```

This will:
- Create a `data_backup.json` file with all your data
- Export users, projects, tasks, finance data, etc.
- Exclude system tables (contenttypes, permissions, sessions)

### Step 4: Run Migrations on PostgreSQL

The import process will automatically run migrations, but you can do it manually:

```bash
python manage.py migrate
```

### Step 5: Import Data to PostgreSQL

Import your exported data to PostgreSQL:

```bash
python migrate_to_postgresql.py import
```

This will:
- Connect to PostgreSQL database
- Run all migrations
- Import all data from `data_backup.json`
- Verify the migration by counting records

### Step 6: Verify Migration

Check that all data was migrated successfully:

```bash
python manage.py shell
```

Then in the Python shell:

```python
from django.contrib.auth.models import User
from projects.models import Project
from finance.models import Account, Transaction
from tasks.models import Task

# Check counts
print(f"Users: {User.objects.count()}")
print(f"Projects: {Project.objects.count()}")
print(f"Tasks: {Task.objects.count()}")
print(f"Accounts: {Account.objects.count()}")
print(f"Transactions: {Transaction.objects.count()}")
```

### Step 7: Test Your Application

```bash
python manage.py runserver
```

Visit `http://localhost:8000` and verify:
- You can log in with your existing account
- All projects are visible
- Finance data is intact
- Tasks are loading correctly

## Quick Migration (All Steps)

```bash
# 1. Install packages
pip install psycopg2-binary dj-database-url

# 2. Verify connection
python migrate_to_postgresql.py verify

# 3. Export from SQLite3
python migrate_to_postgresql.py export

# 4. Import to PostgreSQL
python migrate_to_postgresql.py import

# 5. Test the application
python manage.py runserver
```

## Configuration Files

### .env (Already Created)

```env
DATABASE_URL=postgresql://kennedy:Ybok7619.@157.173.118.68:5432/myhub_db
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1,system.digitalrepublic.space
```

### settings.py (Already Updated)

The database configuration now uses:

```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default=f'sqlite:///{BASE_DIR / "db.sqlite3"}'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}
```

## Troubleshooting

### Connection Errors

**Error:** `could not connect to server`

**Solutions:**
1. Check if PostgreSQL server is running on `157.173.118.68`
2. Verify firewall allows connections on port 5432
3. Test connection with `psql`:
   ```bash
   psql postgresql://kennedy:Ybok7619.@157.173.118.68:5432/myhub_db
   ```

### Import Errors

**Error:** `duplicate key value violates unique constraint`

**Solution:**
- The database might already have data
- Drop all tables and retry:
  ```bash
  python manage.py dbshell
  DROP SCHEMA public CASCADE;
  CREATE SCHEMA public;
  ```

**Error:** `relation does not exist`

**Solution:**
- Run migrations first:
  ```bash
  python manage.py migrate --run-syncdb
  ```

### Package Installation Issues

**Error:** `pg_config executable not found`

**Solution:**
- Use binary package:
  ```bash
  pip install psycopg2-binary
  ```

### Permission Errors

**Error:** `permission denied`

**Solution:**
- Verify user `kennedy` has proper permissions on database `myhub_db`
- Check with database administrator

## Rolling Back to SQLite3

If you need to roll back to SQLite3:

1. Update `.env`:
   ```env
   # DATABASE_URL=postgresql://kennedy:Ybok7619.@157.173.118.68:5432/myhub_db
   DATABASE_URL=sqlite:///db.sqlite3
   ```

2. Restart your application:
   ```bash
   python manage.py runserver
   ```

## PostgreSQL Advantages

Now that you're using PostgreSQL, you get:

✅ **Better Performance** - Faster queries and better indexing
✅ **Concurrent Access** - Multiple users can write simultaneously
✅ **Data Integrity** - ACID compliance and foreign key constraints
✅ **Scalability** - Handles larger datasets efficiently
✅ **Production Ready** - Industry-standard database
✅ **Advanced Features** - JSON fields, full-text search, etc.

## Maintenance Commands

### Backup PostgreSQL Database

```bash
pg_dump postgresql://kennedy:Ybok7619.@157.173.118.68:5432/myhub_db > backup.sql
```

### Restore PostgreSQL Database

```bash
psql postgresql://kennedy:Ybok7619.@157.173.118.68:5432/myhub_db < backup.sql
```

### Check Database Size

```bash
python manage.py dbshell
SELECT pg_size_pretty(pg_database_size('myhub_db'));
```

## Security Notes

🔒 **Important:**
- Never commit `.env` file to version control
- Add `.env` to `.gitignore`
- Use environment variables in production
- Rotate database password periodically
- Use SSL connections in production

## Next Steps

After successful migration:

1. ✅ Delete `data_backup.json` (sensitive data)
2. ✅ Update `.gitignore` to exclude `.env`
3. ✅ Test all application features
4. ✅ Monitor database performance
5. ✅ Set up regular backups
6. ✅ Configure connection pooling if needed

## Support

If you encounter issues:

1. Check the Django logs
2. Review PostgreSQL logs on server
3. Verify network connectivity
4. Test with `migrate_to_postgresql.py verify`

## Summary

Your application is now configured to use PostgreSQL! The migration script makes it easy to move your data safely. Just follow the steps above and you'll be up and running on PostgreSQL in minutes.
