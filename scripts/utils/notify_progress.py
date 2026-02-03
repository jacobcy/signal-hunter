#!/usr/bin/env python3
"""
Notification Utility Script (Town Crier)
Standardizes progress reporting to Telegram.
Uses the new modular reporter and teleporter components.
"""

import argparse
import sys
import os
import asyncio

# Add project root to path to enable imports from src
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.utils.reporter import ReportBuilder
from src.utils.teleporter import Teleporter

# ANSI Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'


async def main():
    parser = argparse.ArgumentParser(description="Send progress notifications to Telegram.")
    parser.add_argument("--task", required=True, help="Task ID or Name")
    parser.add_argument("--agent", required=True, help="Agent Role Name")
    parser.add_argument("--status", required=True, choices=['SUCCESS', 'FAILED', 'SIGNAL'], help="Status of the task")
    parser.add_argument("--problem", help="Problem encountered")
    parser.add_argument("--solution", help="Solution applied")
    parser.add_argument("--next", dest='next_steps', help="Next steps planned")
    parser.add_argument("--report", help="Additional report content")

    args = parser.parse_args()

    # Build the report
    if args.status == 'SIGNAL':
        # For signals, we send the report exactly as provided (no wrapper)
        # unless it's empty, in which case we might default to something
        formatted_message = args.report if args.report else "🚦 SIGNAL DETECTED (No details provided)"
    else:
        # Use the ReportBuilder for standard mission updates
        formatted_message = ReportBuilder.build_mission_update(
            task=args.task,
            agent=args.agent,
            status=args.status,
            problem=args.problem,
            solution=args.solution,
            next_steps=args.next_steps,
            report=args.report
        )

    # Send the message using the Teleporter
    teleporter = Teleporter()
    success = await teleporter.send_with_retry(formatted_message)

    if success:
        print(f"{GREEN}Notification sent successfully.{RESET}")
    else:
        print(f"{RED}Failed to send notification.{RESET}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
