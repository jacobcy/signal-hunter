#!/opt/homebrew/bin/python3
"""
clawd-ops: Unified Operations Tool for OpenClaw

This script provides a central entry point for all operational tasks:
- Environment setup
- System health monitoring  
- Asset testing
- Daily checks
"""

import os
import sys
import argparse
import subprocess
import json
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def run_setup_env():
    """Run environment setup script."""
    print("🔧 Setting up environment...")
    try:
        result = subprocess.run(['bash', str(PROJECT_ROOT / 'scripts' / 'setup_env.sh')], 
                              capture_output=True, text=True, cwd=PROJECT_ROOT)
        if result.returncode == 0:
            print("✅ Environment setup completed successfully")
            return True
        else:
            print(f"❌ Environment setup failed:\n{result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running setup_env.sh: {e}")
        return False

def run_health_check():
    """Run system health check using guardian.py."""
    print("🏥 Running system health check...")
    try:
        from scripts.infrastructure.guardian import main as guardian_main
        # We'll call the guardian directly
        import io
        from contextlib import redirect_stdout, redirect_stderr
        
        # Capture output
        f = io.StringIO()
        with redirect_stdout(f), redirect_stderr(f):
            guardian_main()
        
        output = f.getvalue()
        print("✅ Health check completed")
        if "critical" in output.lower() or "warning" in output.lower():
            print("⚠️  Health check reported issues - see memory/reports/health_latest.json")
        return True
    except Exception as e:
        print(f"❌ Error running health check: {e}")
        return False

def run_asset_test():
    """Run asset testing."""
    print("🔍 Testing critical assets...")
    try:
        from scripts.ops.test_assets import main as test_assets_main
        test_assets_main()
        return True
    except Exception as e:
        print(f"❌ Error running asset tests: {e}")
        return False

def run_daily_check():
    """Run daily project health check."""
    print("📅 Running daily project health check...")
    try:
        result = subprocess.run(['bash', str(PROJECT_ROOT / 'scripts' / 'daily_check.sh')], 
                              capture_output=True, text=True, cwd=PROJECT_ROOT)
        if result.returncode == 0:
            print("✅ Daily check completed successfully")
            # Print the report
            print(result.stdout)
            return True
        else:
            print(f"❌ Daily check failed:\n{result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running daily check: {e}")
        return False

def run_daily_check_telegram():
    """Run daily check with Telegram notification."""
    print("📱 Running daily check with Telegram notification...")
    try:
        from scripts.daily_check_telegram import run_daily_check
        run_daily_check()
        return True
    except Exception as e:
        print(f"❌ Error running daily check with Telegram: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="clawd-ops: Unified Operations Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  clawd-ops setup-env          # Set up environment
  clawd-ops health             # Run system health check  
  clawd-ops test-assets        # Test critical assets
  clawd-ops daily-check        # Run daily project health check
  clawd-ops daily-check-telegram  # Run daily check with Telegram notification
        """
    )
    
    parser.add_argument('command', choices=[
        'setup-env', 'health', 'test-assets', 'daily-check', 'daily-check-telegram'
    ], help='Operation to perform')
    
    args = parser.parse_args()
    
    success = False
    if args.command == 'setup-env':
        success = run_setup_env()
    elif args.command == 'health':
        success = run_health_check()
    elif args.command == 'test-assets':
        success = run_asset_test()
    elif args.command == 'daily-check':
        success = run_daily_check()
    elif args.command == 'daily-check-telegram':
        success = run_daily_check_telegram()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()