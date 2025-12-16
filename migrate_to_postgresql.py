"""
Database Migration Script: SQLite3 to PostgreSQL
This script helps migrate data from SQLite3 to PostgreSQL

Usage:
1. First run: python migrate_to_postgresql.py export
2. Then run: python migrate_to_postgresql.py import
"""
import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myhub.settings')
django.setup()

from django.core.management import call_command
from django.conf import settings
import subprocess


def export_data():
    """Export data from SQLite3 database"""
    print("=" * 60)
    print("STEP 1: Exporting data from SQLite3")
    print("=" * 60)

    # Temporarily use SQLite
    print("\n📦 Backing up current database...")

    fixture_file = 'data_backup.json'

    try:
        print(f"\n💾 Exporting data to {fixture_file}...")
        call_command('dumpdata',
                    '--natural-foreign',
                    '--natural-primary',
                    '--exclude=contenttypes',
                    '--exclude=auth.permission',
                    '--exclude=admin.logentry',
                    '--exclude=sessions.session',
                    '--indent=2',
                    output=fixture_file)

        print(f"✅ Data successfully exported to {fixture_file}")
        print(f"\n📊 File size: {os.path.getsize(fixture_file) / 1024:.2f} KB")

        return True

    except Exception as e:
        print(f"❌ Error exporting data: {e}")
        return False


def import_data():
    """Import data to PostgreSQL database"""
    print("=" * 60)
    print("STEP 2: Importing data to PostgreSQL")
    print("=" * 60)

    fixture_file = 'data_backup.json'

    if not os.path.exists(fixture_file):
        print(f"❌ Error: {fixture_file} not found!")
        print("Please run: python migrate_to_postgresql.py export first")
        return False

    try:
        print("\n🔗 Testing PostgreSQL connection...")
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✅ Connected to PostgreSQL: {version[:50]}...")

        print("\n🔄 Running migrations on PostgreSQL...")
        call_command('migrate', '--run-syncdb')

        print(f"\n📥 Importing data from {fixture_file}...")
        call_command('loaddata', fixture_file)

        print("\n✅ Data successfully imported to PostgreSQL!")

        # Verify data
        print("\n📊 Verifying migration...")
        from django.contrib.auth.models import User
        from projects.models import Project
        from finance.models import Account, Transaction

        print(f"   Users: {User.objects.count()}")
        print(f"   Projects: {Project.objects.count()}")
        print(f"   Finance Accounts: {Account.objects.count()}")
        print(f"   Transactions: {Transaction.objects.count()}")

        print("\n🎉 Migration completed successfully!")
        print(f"\n💡 You can now delete {fixture_file} if everything looks good.")

        return True

    except Exception as e:
        print(f"❌ Error importing data: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Check your DATABASE_URL in .env file")
        print("   2. Ensure PostgreSQL server is accessible")
        print("   3. Verify database credentials")
        return False


def show_help():
    """Show help message"""
    print("""
Database Migration Helper
==========================

This script helps you migrate from SQLite3 to PostgreSQL.

Commands:
    python migrate_to_postgresql.py export    - Export data from SQLite3
    python migrate_to_postgresql.py import    - Import data to PostgreSQL
    python migrate_to_postgresql.py verify    - Verify PostgreSQL connection

Step-by-step process:
    1. Install required packages:
       pip install psycopg2-binary dj-database-url

    2. Update .env with DATABASE_URL (already done)

    3. Export data from SQLite3:
       python migrate_to_postgresql.py export

    4. Import data to PostgreSQL:
       python migrate_to_postgresql.py import

    5. Test your application
    """)


def verify_connection():
    """Verify PostgreSQL connection"""
    print("=" * 60)
    print("PostgreSQL Connection Test")
    print("=" * 60)

    try:
        from django.db import connection

        print(f"\n🔍 Database Engine: {settings.DATABASES['default']['ENGINE']}")
        print(f"📍 Database Name: {settings.DATABASES['default']['NAME']}")
        print(f"🖥️  Host: {settings.DATABASES['default']['HOST']}")
        print(f"🔌 Port: {settings.DATABASES['default']['PORT']}")
        print(f"👤 User: {settings.DATABASES['default']['USER']}")

        print("\n🔗 Testing connection...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"\n✅ Successfully connected to PostgreSQL!")
            print(f"   Version: {version}")

            # Check if tables exist
            cursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema = 'public'
            """)
            table_count = cursor.fetchone()[0]
            print(f"   Tables in database: {table_count}")

        return True

    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Check if PostgreSQL server is running")
        print("   2. Verify .env DATABASE_URL is correct")
        print("   3. Check firewall/network settings")
        print("   4. Ensure psycopg2 is installed: pip install psycopg2-binary")
        return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)

    command = sys.argv[1].lower()

    if command == 'export':
        success = export_data()
        if success:
            print("\n✅ Next step: python migrate_to_postgresql.py import")
        sys.exit(0 if success else 1)

    elif command == 'import':
        success = import_data()
        sys.exit(0 if success else 1)

    elif command == 'verify':
        success = verify_connection()
        sys.exit(0 if success else 1)

    else:
        print(f"❌ Unknown command: {command}")
        show_help()
        sys.exit(1)
