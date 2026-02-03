#!/Users/Jacob/clawd/.venv/bin/python3
"""Daily project health check with Telegram notification."""

import subprocess
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add project to path
sys.path.insert(0, '/Users/Jacob/clawd')

from src.utils.notifier import send_telegram_alert
from src.utils.reporter import ReportBuilder


def run_daily_check():
    """Run the daily check script and send report via Telegram."""
    
    # Run the bash script
    result = subprocess.run(
        ['bash', '/Users/Jacob/clawd/scripts/daily_check.sh'],
        capture_output=True,
        text=True,
        cwd='/Users/Jacob/clawd'
    )
    
    # Get output
    report = result.stdout
    
    if result.returncode != 0:
        report += f"\n\n❌ Script error:\n{result.stderr}"
    
    # Truncate if too long for Telegram (4096 limit)
    if len(report) > 4000:
        report = report[:3900] + "\n\n... (truncated)"
    
    # Send to Telegram
    # Note: This is async but we're in sync context, so we use asyncio
    import asyncio
    
    async def notify():
        try:
            formatted_report = ReportBuilder.build_ai_brief(
                headline="Daily Project Health Check",
                system_audit=report,
            )
            await send_telegram_alert(formatted_report)
            print("✅ Report sent to Telegram")
        except Exception as e:
            print(f"❌ Failed to send Telegram: {e}")
            # Fallback to console
            print(report)
    
    asyncio.run(notify())
    
    # Also save to memory
    timestamp = datetime.now().strftime('%Y-%m-%d')
    report_file = f"/Users/Jacob/clawd/memory/daily-check-{timestamp}.md"
    
    with open(report_file, 'w') as f:
        f.write(f"# Daily Check Report - {timestamp}\n\n")
        f.write(report)
    
    print(f"✅ Report saved to {report_file}")


if __name__ == '__main__':
    run_daily_check()
