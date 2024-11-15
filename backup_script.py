#!/usr/bin/env python3
import os
import shutil
from datetime import datetime, timedelta
import logging
import json
import sys

# Set up logging
logging.basicConfig(filename='backup.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
try:
    with open('backup_config.json', 'r') as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    logging.error("Configuration file not found. Please create backup_config.json")
    sys.exit(1)

SRC_DIR = config.get('source_directory')
DEST_DIR = config.get('destination_directory')
MAX_AGES = tuple(config.get('max_ages', (2, 14, 60)))

def create_backup():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(DEST_DIR, timestamp)
    try:
        shutil.copytree(SRC_DIR, backup_dir)
        logging.info(f"Backup created successfully: {backup_dir}")
    except Exception as e:
        logging.error(f"Failed to create backup: {str(e)}")
        return None
    return timestamp

def clean_dates(dates, now=None, max_ages=MAX_AGES):
    now = now or datetime.now()
    clean = []
    dates.sort()

    for max_age in max_ages:
        older_than_max = [d for d in dates if (now - datetime.strptime(d, '%Y%m%d_%H%M%S')).days < max_age]
        if older_than_max:
            clean.append(older_than_max[0])

    clean.extend(dates[-5:])  # Keep the newest 5
    return sorted(set(clean))  # Remove duplicates and sort

def main():
    try:
        # Create new backup
        new_backup = create_backup()
        if not new_backup:
            return

        # Get list of existing backups
        existing_backups = [d for d in os.listdir(DEST_DIR) if os.path.isdir(os.path.join(DEST_DIR, d))]
        
        # Clean up old backups
        backups_to_keep = clean_dates(existing_backups)
        
        # Remove old backups
        for backup in existing_backups:
            if backup not in backups_to_keep:
                shutil.rmtree(os.path.join(DEST_DIR, backup))
                logging.info(f"Removed old backup: {backup}")

        logging.info("Backup process completed successfully")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
