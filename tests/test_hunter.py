import unittest
import os
import yaml
import sys
import json
from unittest.mock import MagicMock, patch

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hunter.scout import Scout, HunterConfig

class TestHunterConfig(unittest.TestCase):
    """Validation for the configuration file."""
    
    def test_config_structure(self):
        """Ensure config/hunter.yaml is valid YAML and contains required keys."""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'hunter.yaml')
        config_path = os.path.abspath(config_path)
        
        if not os.path.exists(config_path):
            self.skipTest(f"Config file not found at {config_path}")
            
        with open(config_path, 'r') as f:
            try:
                config = yaml.safe_load(f)
            except yaml.YAMLError as e:
                self.fail(f"Config file is not valid YAML: {e}")
        
        self.assertIsInstance(config, dict, "Config must be a dictionary")
        self.assertIn('topics', config, "Config missing 'topics' key")
        self.assertIsInstance(config['topics'], list, "Topics must be a list")

class TestHunterScout(unittest.TestCase):
    """Validation for the Scout logic."""
    
    def setUp(self):
        # Create a temporary config for testing
        self.test_config_data = {
            "topics": [
                {
                    "name": "test_twitter_user_topic",
                    "keywords": ["crypto"],
                    "sources": [
                        {
                            "type": "twitter-user",
                            "query": "@cobie"
                        }
                    ]
                }
            ]
        }
        self.config_path = "tests/temp_hunter_config.yaml"
        with open(self.config_path, 'w') as f:
            yaml.dump(self.test_config_data, f)
            
        self.config = HunterConfig(self.config_path)

    def tearDown(self):
        if os.path.exists(self.config_path):
            os.remove(self.config_path)

    @patch('src.hunter.scout.subprocess.run')
    def test_twitter_user_source(self, mock_subprocess):
        """Verify twitter-user source calls bird user-tweets and parses output."""
        
        # Mock the bird command output
        mock_output = {
            "tweets": [
                {
                    "text": "Crypto is volatile today.",
                    "username": "cobie",
                    "permalink": "https://x.com/cobie/status/123",
                    "created_at": "2023-01-01T12:00:00Z"
                },
                {
                    "text": "Just ate a sandwich.",
                    "username": "cobie",
                    "permalink": "https://x.com/cobie/status/124",
                    "created_at": "2023-01-01T13:00:00Z"
                }
            ]
        }
        
        mock_subprocess.return_value = MagicMock(
            stdout=json.dumps(mock_output),
            returncode=0
        )
        
        scout = Scout(self.config)
        results = scout.hunt()
        
        # Verify subprocess was called correctly
        # We expect: bird user-tweets cobie --json
        # The code strips @, so expected arg is 'cobie'
        expected_cmd = ["bird", "user-tweets", "cobie", "--json"]
        
        # Find the call with these args
        called = False
        for call in mock_subprocess.call_args_list:
            args, _ = call
            if args[0] == expected_cmd:
                called = True
                break
        
        self.assertTrue(called, f"Expected command {expected_cmd} not found in calls: {mock_subprocess.call_args_list}")
        
        # Verify results
        self.assertIn("test_twitter_user_topic", results)
        topic_results = results["test_twitter_user_topic"]
        
        # "Just ate a sandwich" does not contain "crypto", so it should be filtered out
        # "Crypto is volatile today" contains "crypto"
        self.assertEqual(len(topic_results), 1, "Should filter results based on keywords")
        self.assertEqual(topic_results[0]['text'], "Crypto is volatile today.")
        self.assertEqual(topic_results[0]['author'], "cobie")

if __name__ == '__main__':
    unittest.main()
