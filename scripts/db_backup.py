#!/usr/bin/env python3

""" db_backup.py
Backs up the current database and saves the data to JSON files.

Usage: Run from the terminal as such:

Goto the scripts directory:
> cd scripts; ./db_backup.py

Or run from the root of the project:
> scripts/db_backup.py
"""

import sys
import os
import shutil

# Add the directory containing main.py to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app, backup_data

# Backup the database file
def backup_database(db_uri, backup_uri):
    """Creates a backup of the database file if not already backed up."""
    if backup_uri:
        db_path = db_uri.replace('sqlite:///', 'instance/')
        backup_path = backup_uri.replace('sqlite:///', 'instance/')

        if os.path.exists(backup_path):
            print(f"Backup already exists at {backup_path}. Skipping overwrite.")
        else:
            shutil.copyfile(db_path, backup_path)
            print(f"Database backed up to {backup_path}")

def main():
    with app.app_context():
        # Step 1: Backup database data to JSON
        print("Backing up data to JSON files...")
        backup_data()

        # Step 2: Backup the database file safely
        backup_database(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_BACKUP_URI'])

if __name__ == "__main__":
    main()
