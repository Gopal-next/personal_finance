import shutil
import os

# Database path
db_path = 'finance.db'

def backup_database(backup_path='backup_finance.db'):
    """Backup the current database to the specified path."""
    try:
        shutil.copy(db_path, backup_path)
        print(f"Backup successful to {backup_path}")
    except FileNotFoundError:
        print(f"Source database file '{db_path}' does not exist.")
    except PermissionError:
        print(f"Permission denied when trying to access '{db_path}' or '{backup_path}'.")
    except Exception as e:
        print(f"Error during backup: {e}")

def restore_database(backup_path='backup_finance.db'):
    """Restore the database from the specified backup path."""
    if not os.path.exists(backup_path):
        print(f"Backup file '{backup_path}' does not exist.")
        return

    confirmation = input(f"Are you sure you want to restore from '{backup_path}' to '{db_path}'? (yes/no): ")
    if confirmation.lower() != 'yes':
        print("Restore operation canceled.")
        return

    try:
        if os.path.exists(db_path):
            os.remove(db_path)
        shutil.copy(backup_path, db_path)
        print("Database restored successfully.")
    except PermissionError:
        print(f"Permission denied when trying to access '{backup_path}' or '{db_path}'.")
    except Exception as e:
        print(f"Error during restore: {e}")


