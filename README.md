# backup_script

Building a quick script for periodic backups of a folder

## Usage

1. Create a `backup_config.json` file in the root of the project with the following structure:

```
{
    "source_directory": "/path/to/source",
    "destination_directory": "/path/to/backups",
    "max_ages": [2, 14, 60]
}
```

2. Create a service file (e.g. `/etc/systemd/system/backup.service`):

```
[Unit]
Description=Hourly Backup Service

[Service]
ExecStart=/path/to/your/backup_script.py

[Install]
WantedBy=multi-user.target
```

3. Create a timer file (e.g. `/etc/systemd/system/backup.timer`):

```
[Unit]
Description=Run Backup Service Hourly

[Timer]
OnCalendar=hourly

[Install]
WantedBy=timers.target
```

4. Enable and start the timer:

```
sudo systemctl enable backup.timer
sudo systemctl start backup.timer
```

Make sure you have execute permissions for the script:

```
chmod +x backup_script.py
```

## Testing

I made a little test script (`test.py`) to test the backup script as a final sanity check. Make sure you set source and destination directories in the `backup_config.json` file.

To run it:

```
mkdir -p ~/backup_script/demo_src 
mkdir -p ~/backup_script/demo_dst
python test.py
```

And check the `backup.log` file to see the output, plus the `demo_dst` folder to see the backup directories.