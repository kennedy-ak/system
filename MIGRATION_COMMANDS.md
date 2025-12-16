# PostgreSQL Migration - Quick Reference

## 🚀 Run These Commands in Order

### 1. Install Required Packages
```bash
pip install psycopg2-binary dj-database-url
```

### 2. Verify PostgreSQL Connection
```bash
python migrate_to_postgresql.py verify
```

Expected output: ✅ Successfully connected to PostgreSQL

### 3. Export Data from SQLite3
```bash
python migrate_to_postgresql.py export
```

This creates `data_backup.json` with all your data.

### 4. Import Data to PostgreSQL
```bash
python migrate_to_postgresql.py import
```

This will:
- Run all migrations on PostgreSQL
- Import all your data
- Verify the migration

### 5. Test Your Application
```bash
python manage.py runserver
```

Visit http://localhost:8000 and verify everything works!

---

## ✅ What's Already Done

- ✅ Created `.env` with PostgreSQL connection string
- ✅ Updated `settings.py` to use `DATABASE_URL`
- ✅ Created migration script (`migrate_to_postgresql.py`)
- ✅ Updated `requirements.txt` with new packages
- ✅ Updated `.gitignore` to exclude sensitive files

---

## 📊 Check Migration Success

```bash
python manage.py shell
```

Then run:
```python
from django.contrib.auth.models import User
from projects.models import Project
from finance.models import Account

print(f"Users: {User.objects.count()}")
print(f"Projects: {Project.objects.count()}")
print(f"Accounts: {Account.objects.count()}")
```

---

## 🔧 Troubleshooting

### If connection fails:
```bash
python migrate_to_postgresql.py verify
```

### If import fails:
1. Check `.env` file has correct DATABASE_URL
2. Ensure PostgreSQL server is accessible
3. Verify credentials are correct

### Roll back to SQLite (if needed):
Edit `.env` and comment out DATABASE_URL:
```env
# DATABASE_URL=postgresql://kennedy:Ybok7619.@157.173.118.68:5432/myhub_db
```

---

## 🎯 That's It!

Just run these 4 commands and you're migrated to PostgreSQL! 🎉
