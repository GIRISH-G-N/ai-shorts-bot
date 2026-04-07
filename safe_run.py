"""
safe_run.py
Runs a script with automatic retries and clean error reporting.
"""

import subprocess
import sys
import time


def safe_run(script, *args, retries=3, wait=10):
    for attempt in range(1, retries + 1):
        try:
            print(f"\n▶  {script} {'  '.join(args)} (attempt {attempt}/{retries})")
            subprocess.run([sys.executable, script, *args], check=True)
            print(f"✅ {script} done")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ {script} failed")
            if attempt < retries:
                print(f"⏳ Retrying in {wait}s...")
                time.sleep(wait)
            else:
                print(f"🚨 Giving up on {script}")
                return False
