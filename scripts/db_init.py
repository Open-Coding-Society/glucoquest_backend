#!/usr/bin/env python3

""" db_init.py
Generates the database schema for all db models.
- Initializes Users, Sections, and UserSections tables.
- Imports data from the old database to the new database.

Usage: Run from the terminal as such:

Goto the scripts directory:
> cd scripts; ./db_init.py

Or run from the root of the project:
> scripts/db_init.py
"""

import shutil
import sys
import os

# Add the directory containing main.py to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app, db, generate_data

# Backup the old database
def backup_database(db_uri, backup_uri):
    """Backup the current database without overwriting an existing backup."""
    if backup_uri:
        db_path = db_uri.replace('sqlite:///', 'instance/')
        backup_path = backup_uri.replace('sqlite:///', 'instance/')

        if os.path.exists(backup_path):
            print(f"Backup already exists at {backup_path}. Skipping overwrite.")
        else:
            shutil.copyfile(db_path, backup_path)
            print(f"Database backed up to {backup_path}")
    else:
        print("Backup not supported for production database.")

# Main extraction and loading process
def main():
    # Step 0: Warning to the user and backup database
    with app.app_context():
        try:
            # Check if database has tables
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            if tables:
                print("Warning, you are about to lose all data in the database!")
                print("Do you want to continue? (y/n)")
                response = input()
                if response.lower() != 'y':
                    print("Exiting without making changes.")
                    sys.exit(0)

            # Backup the current database (if no backup exists)
            backup_database(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_BACKUP_URI'])
        
        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit(1)

    # Step 1: Reinitialize database (but do not modify the backup)
    try:
        with app.app_context():
            # Drop and recreate tables in the main database only
            db.drop_all()
            print("All tables dropped.")

            print("Generating data.")
            generate_data()
            
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    print("Database initialized!")

if __name__ == "__main__":
    main()
