#!/usr/bin/env python3
"""
Asset testing utility for critical infrastructure components.
Tests API keys, file paths, network connectivity, and other critical assets.
"""

import os
import sys
import json
import socket
import urllib.request
import urllib.error
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv()


class AssetTester:
    """Test various critical assets for the OpenClaw system."""
    
    def __init__(self):
        self.results = {}
        self.project_root = project_root
        
    def test_file_paths(self):
        """Test critical file paths exist and are accessible."""
        critical_files = [
            ".env",
            "openclaw.json",
            "requirements.txt",
            ".venv/bin/python",
            "scripts/infrastructure/guardian.py"
        ]
        
        missing_files = []
        for file_path in critical_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                missing_files.append(file_path)
                
        if missing_files:
            self.results['file_paths'] = {
                'status': 'critical',
                'message': f'Missing critical files: {", ".join(missing_files)}'
            }
        else:
            self.results['file_paths'] = {
                'status': 'ok',
                'message': 'All critical files present'
            }
            
    def test_network_connectivity(self):
        """Test basic network connectivity."""
        try:
            # Test DNS resolution and connectivity
            socket.create_connection(("8.8.8.8", 53), timeout=5)
            self.results['network'] = {
                'status': 'ok',
                'message': 'Internet connectivity confirmed'
            }
        except OSError:
            self.results['network'] = {
                'status': 'critical',
                'message': 'No internet connectivity'
            }
            
    def test_api_endpoints(self):
        """Test critical API endpoints."""
        api_tests = []
        
        # Test Telegram API
        try:
            socket.create_connection(("api.telegram.org", 443), timeout=10)
            api_tests.append("Telegram API: reachable")
        except Exception as e:
            api_tests.append(f"Telegram API: unreachable - {str(e)}")
            
        # Test OpenAI API (if key available)
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            try:
                socket.create_connection(("api.openai.com", 443), timeout=10)
                api_tests.append("OpenAI API: reachable")
            except Exception as e:
                api_tests.append(f"OpenAI API: unreachable - {str(e)}")
        else:
            api_tests.append("OpenAI API: key not configured")
            
        # Test OpenRouter API (if key available)
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        if openrouter_key:
            try:
                socket.create_connection(("openrouter.ai", 443), timeout=10)
                api_tests.append("OpenRouter API: reachable")
            except Exception as e:
                api_tests.append(f"OpenRouter API: unreachable - {str(e)}")
        else:
            api_tests.append("OpenRouter API: key not configured")
            
        # Determine overall status
        unreachable_count = sum(1 for test in api_tests if "unreachable" in test)
        if unreachable_count > 0:
            status = "warning" if unreachable_count < len(api_tests) else "critical"
        else:
            status = "ok"
            
        self.results['api_endpoints'] = {
            'status': status,
            'message': '; '.join(api_tests)
        }
        
    def test_venv(self):
        """Test virtual environment activation."""
        venv_path = self.project_root / ".venv"
        if venv_path.exists() and (venv_path / "bin" / "python").exists():
            self.results['venv'] = {
                'status': 'ok',
                'message': 'Virtual environment ready'
            }
        else:
            self.results['venv'] = {
                'status': 'critical',
                'message': 'Virtual environment not found or incomplete'
            }
            
    def run_all_tests(self):
        """Run all asset tests."""
        print("🔍 Testing critical assets...")
        self.test_file_paths()
        self.test_network_connectivity()
        self.test_api_endpoints()
        self.test_venv()
        
        # Print results
        print("\n📊 Asset Test Results:")
        print("=" * 50)
        
        overall_status = "ok"
        for test_name, result in self.results.items():
            status = result['status']
            message = result['message']
            
            if status == "critical":
                print(f"❌ {test_name}: {message}")
                overall_status = "critical"
            elif status == "warning":
                print(f"⚠️  {test_name}: {message}")
                if overall_status != "critical":
                    overall_status = "warning"
            else:
                print(f"✅ {test_name}: {message}")
                
        print("=" * 50)
        if overall_status == "ok":
            print("🎉 All assets are healthy!")
        elif overall_status == "warning":
            print("⚠️  Some assets need attention.")
        else:
            print("🚨 Critical asset failures detected!")
            
        return overall_status, self.results


def main():
    """Main entry point."""
    tester = AssetTester()
    status, results = tester.run_all_tests()
    
    # Exit with appropriate code
    if status == "critical":
        sys.exit(1)
    elif status == "warning":
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()