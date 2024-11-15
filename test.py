import os
import shutil
import time
from datetime import datetime, timedelta
from backup_script import DEST_DIR, main

def generate_test_dates(num_dates, base_date):
    return [(base_date + timedelta(hours=i)).strftime("%Y%m%d_%H%M%S") for i in range(num_dates)]

def create_fake_backups(dates):
    """Create fake backup directories with the given dates"""
    for date in dates:
        backup_dir = os.path.join(DEST_DIR, date)
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            # Create a dummy file in each backup directory
            with open(os.path.join(backup_dir, 'dummy.txt'), 'w') as f:
                f.write(f"Test backup created at {date}")

def cleanup_test_backups():
    """Remove all test backups"""
    if os.path.exists(DEST_DIR):
        shutil.rmtree(DEST_DIR)
    os.makedirs(DEST_DIR)

def run_test():
    # Clean up any existing backups
    cleanup_test_backups()
    
    # Generate test dates starting from 100 days ago
    base_date = datetime.now() - timedelta(days=100)
    test_dates = generate_test_dates(2400, base_date)  # Creates dates over 100 days
    
    # Create fake backup directories
    create_fake_backups(test_dates)
    print(f"Created {len(test_dates)} fake backups")
    
    # Run the backup script multiple times
    for i in range(3):
        print(f"\nRunning backup script iteration {i+1}")
        main()
        time.sleep(2)
        
        # Count remaining backups
        remaining = len([d for d in os.listdir(DEST_DIR) if os.path.isdir(os.path.join(DEST_DIR, d))])
        print(f"Remaining backups after cleanup: {remaining}")

if __name__ == "__main__":
    run_test()

