import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
import os
import json

# Add project root to path to allow imports once the file exists
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# We try to import the module. If it doesn't exist yet (Dev hasn't finished), 
# we can skip the tests or use a dummy for syntax checking.
try:
    from scripts.infrastructure import guardian
except ImportError:
    guardian = None

class TestSystemHealthGuardian(unittest.TestCase):

    def setUp(self):
        if guardian is None:
            self.skipTest("Guardian module not found. Waiting for Dev to implement scripts/infrastructure/guardian.py")
        self.guardian_instance = guardian.SystemGuardian()

    @patch('scripts.infrastructure.guardian.subprocess.run')
    def test_connectivity_success(self, mock_subprocess):
        """Test that connectivity check returns True when ping succeeds."""
        # Mock ping return code 0 (success)
        mock_subprocess.return_value = MagicMock(returncode=0)
        
        result = self.guardian_instance.check_connectivity()
        self.assertTrue(result['status'])
        self.assertEqual(result['component'], 'connectivity')

    @patch('scripts.infrastructure.guardian.subprocess.run')
    def test_connectivity_failure(self, mock_subprocess):
        """Test that connectivity check returns False when ping fails."""
        # Mock ping return code 1 (failure)
        mock_subprocess.return_value = MagicMock(returncode=1)
        
        result = self.guardian_instance.check_connectivity()
        self.assertFalse(result['status'])

    @patch('scripts.infrastructure.guardian.requests.get')
    def test_telegram_api_valid(self, mock_get):
        """Test Telegram API check returns True on 200 OK with correct payload."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ok": True, "result": {"username": "test_bot"}}
        mock_get.return_value = mock_response

        result = self.guardian_instance.check_telegram()
        self.assertTrue(result['status'])

    @patch('scripts.infrastructure.guardian.requests.get')
    def test_telegram_api_invalid(self, mock_get):
        """Test Telegram API check returns False on 401 Unauthorized."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        result = self.guardian_instance.check_telegram()
        self.assertFalse(result['status'])

    @patch('scripts.infrastructure.guardian.shutil.disk_usage')
    def test_disk_usage_healthy(self, mock_disk):
        """Test disk usage returns healthy when usage is low."""
        # total, used, free
        mock_disk.return_value = (1000, 200, 800) # 20% used
        
        result = self.guardian_instance.check_resources()
        self.assertTrue(result['status'])

    @patch('scripts.infrastructure.guardian.shutil.disk_usage')
    def test_disk_usage_warning(self, mock_disk):
        """Test disk usage returns warning/False when usage is > 90%."""
        # total, used, free
        mock_disk.return_value = (1000, 950, 50) # 95% used
        
        result = self.guardian_instance.check_resources()
        # Depending on implementation, this might be False (fail) or True with warning message
        # Assuming requirement says ">90% alert", so status might be False or 'warning'
        # For this test, let's assume it flags as False (unhealthy)
        self.assertFalse(result['status'])
        self.assertIn("Disk usage critical", result.get('message', ''))

    @patch('scripts.infrastructure.guardian.socket.socket')
    def test_openclaw_process_check(self, mock_socket):
        """Test OpenClaw port check."""
        mock_sock_instance = MagicMock()
        mock_socket.return_value = mock_sock_instance
        
        # connect_ex returning 0 means success (port open)
        mock_sock_instance.connect_ex.return_value = 0
        
        result = self.guardian_instance.check_openclaw_process()
        self.assertTrue(result['status'])

    @patch('builtins.open', new_callable=mock_open)
    @patch('scripts.infrastructure.guardian.SystemGuardian.run_all_checks')
    def test_report_generation(self, mock_run_checks, mock_file):
        """Test that a JSON report is written to the correct location."""
        mock_run_checks.return_value = {
            "timestamp": "2023-01-01T12:00:00",
            "checks": []
        }
        
        # Trigger the main execution or report saving method
        self.guardian_instance.save_report()
        
        # Verify file write to memory/reports/health_latest.json
        mock_file.assert_called_with('memory/reports/health_latest.json', 'w')
        handle = mock_file()
        handle.write.assert_called()

if __name__ == '__main__':
    unittest.main()
