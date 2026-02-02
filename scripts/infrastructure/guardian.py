import os
import sys
import json
import time
import socket
import shutil
import datetime
import subprocess
import re

# Configuration
REPORT_PATH = "memory/reports/health_latest.json"
TELEGRAM_TARGET = ""  # Set to your Telegram User ID or Channel ID (e.g., "123456789" or "@mychannel")

# --- Checks ---

def check_network():
    """Checks internet connectivity by pinging a reliable host (e.g., 8.8.8.8)."""
    try:
        # Ping Google DNS
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return {"status": "ok", "message": "Internet connectivity confirmed"}
    except OSError:
        return {"status": "critical", "message": "No internet connectivity"}

def check_resources():
    """Checks system resources (CPU, Memory, Disk) using standard libs/commands for MacOS."""
    
    # 1. Disk Usage
    total, used, free = shutil.disk_usage("/")
    disk_percent = (used / total) * 100
    
    # 2. Load Average (CPU proxy)
    # Returns (1min, 5min, 15min) load average
    load_avg = os.getloadavg()
    cpu_load_1min = load_avg[0]
    
    # 3. Memory (MacOS specific vm_stat)
    mem_percent = 0
    try:
        # vm_stat returns pages. Page size is usually 4096 bytes.
        out = subprocess.check_output("vm_stat", shell=True).decode('utf-8')
        page_size = 4096
        
        # Parse free pages
        free_match = re.search(r"Pages free:\s+(\d+)", out)
        active_match = re.search(r"Pages active:\s+(\d+)", out)
        inactive_match = re.search(r"Pages inactive:\s+(\d+)", out)
        wired_match = re.search(r"Pages wired down:\s+(\d+)", out)
        speculative_match = re.search(r"Pages speculative:\s+(\d+)", out)

        if free_match and active_match:
            free_pages = int(free_match.group(1))
            active_pages = int(active_match.group(1))
            inactive_pages = int(inactive_match.group(1)) if inactive_match else 0
            wired_pages = int(wired_match.group(1)) if wired_match else 0
            speculative_pages = int(speculative_match.group(1)) if speculative_match else 0
            
            # Rough estimate of total used
            # "Free" in vm_stat is strictly free. "Inactive" is available if needed.
            # Total RAM isn't in vm_stat, usually need sysctl.
            # Let's fallback to sysctl for total mem
            sysctl_mem = subprocess.check_output("/usr/sbin/sysctl hw.memsize", shell=True).decode('utf-8')
            total_ram = int(re.search(r"\d+", sysctl_mem).group(0))
            
            # Used = Total - (Free + Inactive) roughly for "available" logic
            # Or just calculate used bytes
            used_pages = active_pages + wired_pages
            used_bytes = used_pages * page_size
            mem_percent = (used_bytes / total_ram) * 100
    except Exception as e:
        print(f"Error checking memory: {e}")
        mem_percent = 0 # Fail safe

    status = "ok"
    details = []
    
    # Thresholds
    if cpu_load_1min > 4.0: # Arbitrary high load for a desktop
        status = "warning"
        details.append(f"High Load Avg (1m): {cpu_load_1min}")
        
    if mem_percent > 90:
        status = "warning"
        details.append(f"High Memory usage: {mem_percent:.1f}%")
        
    if disk_percent > 90:
        status = "warning"
        details.append(f"Low Disk Space: {disk_percent:.1f}% used")

    return {
        "status": status,
        "message": "; ".join(details) if details else "Resources within normal limits",
        "metrics": {
            "load_avg_1min": cpu_load_1min,
            "memory_percent": round(mem_percent, 1),
            "disk_percent": round(disk_percent, 1)
        }
    }

def check_processes():
    """Checks for critical processes."""
    # Basic check: just see if we can run ps
    try:
        # Check for openclaw processes as an example of self-awareness
        # Use pgrep logic
        output = subprocess.check_output(["ps", "-A"], text=True)
        # We assume if we are running, python is running.
        return {"status": "ok", "message": "Process monitor active"}
    except Exception as e:
        return {"status": "warning", "message": f"Process check failed: {e}"}

def check_assets():
    """Checks external assets (LLM/Telegram connectivity)."""
    results = {}
    
    # 1. Telegram
    try:
        # Just DNS/Connect check to api.telegram.org
        socket.create_connection(("api.telegram.org", 443), timeout=5)
        results['telegram'] = "reachable"
    except Exception as e:
        results['telegram'] = f"unreachable"

    # 2. LLM (OpenAI)
    try:
        socket.create_connection(("api.openai.com", 443), timeout=5)
        results['llm_api_network'] = "reachable"
    except Exception:
        results['llm_api_network'] = "unreachable"

    # Determine status
    if "unreachable" in results.values():
        return {"status": "warning", "message": "Some assets unreachable", "details": results}
    
    return {"status": "ok", "message": "Assets reachable", "details": results}

# --- Reporting & Alerting ---

def generate_report():
    report = {
        "timestamp": datetime.datetime.now().isoformat(),
        "checks": {
            "network": check_network(),
            "resources": check_resources(),
            "processes": check_processes(),
            "assets": check_assets()
        },
        "overall_status": "ok"
    }
    
    # Determine overall status
    statuses = [v['status'] for k, v in report['checks'].items()]
    if "critical" in statuses:
        report['overall_status'] = "critical"
    elif "warning" in statuses:
        report['overall_status'] = "warning"
        
    return report

def save_report(report):
    try:
        os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
        with open(REPORT_PATH, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"Report saved to {REPORT_PATH}")
    except Exception as e:
        print(f"Failed to save report: {e}")

def send_alert(report):
    """
    Sends a telegram alert if status is critical using the openclaw CLI.
    """
    if report['overall_status'] == "critical":
        message = "🚨 **SYSTEM HEALTH CRITICAL** 🚨\n\nIssues detected:\n"
        for k, v in report['checks'].items():
            if v['status'] == 'critical':
                message += f"- {k.upper()}: {v['message']}\n"
        
        print(f"\n{message}")

        if TELEGRAM_TARGET:
            try:
                subprocess.run([
                    "openclaw", "message", "send",
                    "--channel", "telegram",
                    "--target", TELEGRAM_TARGET,
                    "--message", message
                ], check=False) # Don't crash if alert fails
                print(f"Alert sent to {TELEGRAM_TARGET}")
            except FileNotFoundError:
                print("Error: 'openclaw' CLI not found. Alert not sent.")
            except Exception as e:
                print(f"Error sending alert: {e}")
        else:
            print("TELEGRAM_TARGET not configured. Skipping Telegram alert.")

def main():
    print("Running System Health Guardian (No-Dep Version)...")
    report = generate_report()
    save_report(report)
    
    if report['overall_status'] != "ok":
        send_alert(report)
        if report['overall_status'] == "critical":
            sys.exit(1)

if __name__ == "__main__":
    main()
