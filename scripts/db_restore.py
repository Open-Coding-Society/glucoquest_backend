#!/usr/bin/env python3

""" db_restore.py
Restores the database from JSON files and optionally from the backup database.

Usage: Run from the terminal as such:

Goto the scripts directory:
> cd scripts; ./db_restore.py

Or run from the root of the project:
> scripts/db_restore.py
"""

import sys
import os
import shutil

# Add the directory containing main.py to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app, restore_data_command

def restore_database(backup_uri, db_uri):
    """Restore the database from backup file if available."""
    if backup_uri:
        backup_path = backup_uri.replace('sqlite:///', 'instance/')
        db_path = db_uri.replace('sqlite:///', 'instance/')

        if os.path.exists(backup_path):
            if os.path.exists(db_path):
                print(f"Database already exists at {db_path}. Skipping restore from backup.")
            else:
                shutil.copyfile(backup_path, db_path)
                print(f"Database restored from {backup_path}")
        else:
            print("No backup database found. Skipping backup restore.")

def main():
    with app.app_context():
        # Step 1: Restore database file first
        restore_database(app.config['SQLALCHEMY_BACKUP_URI'], app.config['SQLALCHEMY_DATABASE_URI'])

        # Step 2: Restore JSON data
        print("Restoring data from JSON files...")
        restore_data_command()

if __name__ == "__main__":
    main()
