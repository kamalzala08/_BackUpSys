import sched
import time
import datetime
import subprocess

def run_backup():
    # Replace this with the path to your backup script
    subprocess.call(['/usr/bin/python3', '/home/kamal/Documents/COLLAGE/SEM-6/DSS/BackUpSys/main.py'])

# Create a scheduler object
scheduler = sched.scheduler(time.time, time.sleep)

# Calculate the time for the first backup (2am tomorrow)
now = datetime.datetime.now()
next_backup = now.replace(hour=0, minute=0, second=30, microsecond=0) + datetime.timedelta(days=1)

# Schedule the backup to run every day at 2am
while True:
    # Calculate the delay until the next backup
    delay = (next_backup - datetime.datetime.now()).total_seconds()

    # Schedule the backup to run at the next_backup time
    scheduler.enter(delay, 1, run_backup, ())

    # Update the next_backup time to be 24 hours from now
    next_backup = next_backup + datetime.timedelta(days=1)

    # Run the scheduler
    scheduler.run()
