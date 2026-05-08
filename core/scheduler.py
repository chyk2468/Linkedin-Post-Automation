import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).parent.parent
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

import schedule
import time
import datetime
from core.automation import AutomationPipeline
from core.logger import get_last_post_date

def job():
    print(f"\n⏰ Scheduled job triggered at {datetime.datetime.now()}")
    
    # Safety check: Don't post twice in one day
    last_date = get_last_post_date()
    if last_date == datetime.date.today():
        print("ℹ️ Already posted today. Skipping scheduled job.")
        return

    pipeline = AutomationPipeline()
    pipeline.run()

def main():
    print("🤖 LinkedIn Automation Manual Trigger")
    print("ℹ️ Automated scheduling has been disabled as requested.")
    print("🚀 Triggering a single run now...")
    
    job()

if __name__ == "__main__":
    main()
