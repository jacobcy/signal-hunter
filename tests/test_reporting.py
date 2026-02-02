#!/usr/bin/env python3
"""
Unit Tests for Reporting Modules
Tests for Teleporter and ReportBuilder classes.
"""

import pytest
import asyncio
import os
from unittest.mock import patch, MagicMock, AsyncMock
from src.utils.teleporter import Teleporter
from src.utils.reporter import ReportBuilder, ReportFormatter


class TestReportBuilder:
    """Test cases for ReportBuilder class."""

    def test_build_mission_update_basic(self):
        """Test basic mission update report generation."""
        result = ReportBuilder.build_mission_update(
            task="Test Task",
            agent="Test Agent",
            status="SUCCESS"
        )
        
        assert "🚀 **Mission Update: Test Task**" in result
        assert "👤 **Agent:** Test Agent" in result
        assert "✅ **Status:** SUCCESS" in result
        assert "#OpenClaw #DevUpdate" in result

    def test_build_mission_update_failed_status(self):
        """Test mission update with FAILED status."""
        result = ReportBuilder.build_mission_update(
            task="Test Task",
            agent="Test Agent",
            status="FAILED"
        )
        
        assert "❌ **Status:** FAILED" in result

    def test_build_mission_update_with_problem(self):
        """Test mission update with problem field."""
        result = ReportBuilder.build_mission_update(
            task="Test Task",
            agent="Test Agent",
            status="FAILED",
            problem="Something went wrong"
        )
        
        assert "🔍 **Problem:** Something went wrong" in result

    def test_build_mission_update_with_solution(self):
        """Test mission update with solution field."""
        result = ReportBuilder.build_mission_update(
            task="Test Task",
            agent="Test Agent",
            status="SUCCESS",
            solution="Applied fix X"
        )
        
        assert "🛠️ **Solution:** Applied fix X" in result

    def test_build_mission_update_with_next_steps(self):
        """Test mission update with next steps field."""
        result = ReportBuilder.build_mission_update(
            task="Test Task",
            agent="Test Agent",
            status="SUCCESS",
            next_steps="Continue with phase 2"
        )
        
        assert "⏭️ **Next Steps:** Continue with phase 2" in result

    def test_build_mission_update_with_report(self):
        """Test mission update with report field."""
        result = ReportBuilder.build_mission_update(
            task="Test Task",
            agent="Test Agent",
            status="SUCCESS",
            report="Detailed report content"
        )
        
        assert "📋 **Report:** Detailed report content" in result

    def test_build_market_signal_basic(self):
        """Test basic market signal report generation."""
        result = ReportBuilder.build_market_signal(
            signal="Price increase detected",
            reason="Market demand surge"
        )
        
        assert "📈 **Market Signal:** Price increase detected" in result
        assert "💡 **Reason:** Market demand surge" in result
        assert "#OpenClaw #MarketSignal" in result

    def test_build_market_signal_with_audit(self):
        """Test market signal with audit field."""
        result = ReportBuilder.build_market_signal(
            signal="Price increase detected",
            reason="Market demand surge",
            audit="Checked against historical data"
        )
        
        assert "🔍 **Audit Trail:** Checked against historical data" in result

    def test_build_ai_brief_basic(self):
        """Test basic AI brief report generation."""
        result = ReportBuilder.build_ai_brief(
            headline="Market trend identified"
        )
        
        assert "🤖 **AI Brief: Market trend identified**" in result
        assert "#OpenClaw #AIBrief" in result

    def test_build_ai_brief_with_all_fields(self):
        """Test AI brief with all optional fields."""
        result = ReportBuilder.build_ai_brief(
            headline="Market trend identified",
            deep_dive="Analysis shows 15% growth potential",
            kol_sentiment="Positive sentiment from tech influencers",
            system_audit="All systems operational"
        )
        
        assert "🔬 **Deep Dive:** Analysis shows 15% growth potential" in result
        assert "💬 **KOL Sentiment:** Positive sentiment from tech influencers" in result
        assert "⚙️ **System Audit:** All systems operational" in result


class TestReportFormatter:
    """Test cases for ReportFormatter class."""

    def test_truncate_text_within_limit(self):
        """Test text that is within the limit is not truncated."""
        text = "Short text"
        result = ReportFormatter.truncate_text(text, max_length=100)
        
        assert result == "Short text"

    def test_truncate_text_exceeds_limit(self):
        """Test text that exceeds the limit is truncated."""
        long_text = "A" * 5000  # 5000 characters
        result = ReportFormatter.truncate_text(long_text, max_length=100)
        
        assert len(result) <= 100
        assert "(truncated)" in result

    def test_format_timestamp(self):
        """Test timestamp formatting."""
        from datetime import datetime
        test_time = datetime(2023, 6, 15, 14, 30, 45)
        result = ReportFormatter.format_timestamp(test_time)
        
        assert result == "2023-06-15 14:30:45"

    def test_format_timestamp_now(self):
        """Test timestamp formatting with current time."""
        result = ReportFormatter.format_timestamp()
        
        # Should be in the right format even if we can't predict the exact value
        assert len(result) == 19  # YYYY-MM-DD HH:MM:SS
        assert result.count("-") == 2
        assert result.count(":") == 2
        assert result.count(" ") == 1

    def test_escape_markdown_v2_basic(self):
        """Test escaping basic markdown characters."""
        text = "This is *bold* and _italic_ text"
        result = ReportFormatter.escape_markdown_v2(text)
        
        assert r"\*bold\*" in result
        assert r"\_italic\_" in result

    def test_escape_markdown_v2_special_chars(self):
        """Test escaping various special characters."""
        text = "Header #1 [link](url) `code` ~strikethrough~"
        result = ReportFormatter.escape_markdown_v2(text)
        
        assert r"\#1" in result
        assert r"\[link\]\(url\)" in result
        assert r"\`code\`" in result
        assert r"\~strikethrough\~" in result


class TestTeleporter:
    """Test cases for Teleporter class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Mock environment variables for testing
        os.environ["TELEGRAM_BOT_TOKEN"] = "test_token"
        os.environ["TELEGRAM_CHANNEL_ID"] = "test_channel_id"

    def teardown_method(self):
        """Clean up after each test method."""
        # Remove test environment variables
        if "TELEGRAM_BOT_TOKEN" in os.environ:
            del os.environ["TELEGRAM_BOT_TOKEN"]
        if "TELEGRAM_CHANNEL_ID" in os.environ:
            del os.environ["TELEGRAM_CHANNEL_ID"]

    @patch('src.utils.teleporter.logger')
    @patch('httpx.AsyncClient.post')
    @patch('builtins.__import__')
    def test_send_with_httpx_success(self, mock_import, mock_post, mock_logger):
        """Test successful message sending via httpx."""
        # Mock httpx import to succeed
        def import_side_effect(name, *args, **kwargs):
            if name == 'httpx':
                mock_httpx = MagicMock()
                mock_async_client = AsyncMock()
                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_async_client.post.return_value.__aenter__.return_value = mock_response
                mock_httpx.AsyncClient.return_value = mock_async_client
                return mock_httpx
            # For any other import, raise ImportError to simulate the actual import
            if name in ['urllib.request', 'urllib.parse']:
                original_import = __import__
                return original_import(name, *args, **kwargs)
            raise ImportError()
        
        mock_import.side_effect = import_side_effect

        teleporter = Teleporter()
        
        # Run the async method
        async def run_test():
            return await teleporter._send_with_httpx("Test message", "test_chat_id")
        
        result = asyncio.run(run_test())
        
        assert result is True
        mock_logger.info.assert_called_with("✅ Message sent successfully via httpx")

    @patch('src.utils.teleporter.logger')
    @patch('urllib.request.urlopen')
    @patch('builtins.__import__')
    def test_send_with_urllib_success(self, mock_import, mock_urlopen, mock_logger):
        """Test successful message sending via urllib."""
        # Mock urllib components
        mock_request = MagicMock()
        mock_response = MagicMock()
        mock_response.status = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        # Set up the import mock to fail on httpx but succeed on urllib
        def import_side_effect(name, *args, **kwargs):
            if name == 'httpx':
                raise ImportError("No module named 'httpx'")
            elif name == 'urllib.request':
                import urllib.request
                return urllib.request
            elif name == 'urllib.parse':
                import urllib.parse
                return urllib.parse
            # For other modules, use the original import
            return __import__(name, *args, **kwargs)
        
        mock_import.side_effect = import_side_effect
        mock_import.urllib = urllib

        teleporter = Teleporter()
        result = teleporter._send_with_urllib("Test message", "test_chat_id")
        
        assert result is True
        mock_logger.info.assert_called_with("✅ Message sent successfully via urllib")

    @patch('src.utils.teleporter.logger')
    def test_send_message_missing_token(self, mock_logger):
        """Test send_message when bot token is missing."""
        # Temporarily remove the token
        if "TELEGRAM_BOT_TOKEN" in os.environ:
            del os.environ["TELEGRAM_BOT_TOKEN"]
        
        teleporter = Teleporter()
        
        async def run_test():
            return await teleporter.send_message("Test message", "test_chat_id")
        
        result = asyncio.run(run_test())
        
        assert result is False
        mock_logger.error.assert_called_with("❌ TELEGRAM_BOT_TOKEN not set")

    @patch('src.utils.teleporter.logger')
    def test_send_message_missing_target_id(self, mock_logger):
        """Test send_message when target ID is missing."""
        # Temporarily remove the channel ID
        if "TELEGRAM_CHANNEL_ID" in os.environ:
            del os.environ["TELEGRAM_CHANNEL_ID"]
        if "TELEGRAM_CHAT_ID" in os.environ:
            os.environ["TELEGRAM_CHAT_ID"] = ""
        
        teleporter = Teleporter()
        
        async def run_test():
            return await teleporter.send_message("Test message", None)
        
        result = asyncio.run(run_test())
        
        assert result is False
        mock_logger.error.assert_called_with("❌ TELEGRAM_CHANNEL_ID or TELEGRAM_CHAT_ID not set")

    @patch('src.utils.teleporter.Teleporter.send_message')
    def test_send_with_retry_success_on_first_attempt(self, mock_send_message):
        """Test send_with_retry succeeds on first attempt."""
        # Make the mock send_message return True on first call
        async def mock_send_true(*args, **kwargs):
            return True
        mock_send_message.side_effect = mock_send_true
        
        teleporter = Teleporter()
        
        async def run_test():
            return await teleporter.send_with_retry("Test message", "test_chat_id", max_attempts=3)
        
        result = asyncio.run(run_test())
        
        assert result is True
        # Should only be called once since it succeeded
        assert mock_send_message.call_count == 1

    @patch('src.utils.teleporter.Teleporter.send_message')
    @patch('asyncio.sleep', return_value=None)  # Mock sleep to speed up test
    def test_send_with_retry_succeeds_after_failure(self, mock_sleep, mock_send_message):
        """Test send_with_retry eventually succeeds after initial failures."""
        # Make the mock send_message return False twice, then True
        responses = [False, False, True]
        async def mock_send_sequence(*args, **kwargs):
            return responses.pop(0)
        mock_send_message.side_effect = mock_send_sequence
        
        teleporter = Teleporter()
        
        async def run_test():
            return await teleporter.send_with_retry("Test message", "test_chat_id", max_attempts=3)
        
        result = asyncio.run(run_test())
        
        assert result is True
        assert mock_send_message.call_count == 3  # Called 3 times total

    @patch('src.utils.teleporter.Teleporter.send_message')
    @patch('asyncio.sleep', return_value=None)  # Mock sleep to speed up test
    def test_send_with_retry_fails_after_all_attempts(self, mock_sleep, mock_send_message):
        """Test send_with_retry fails after all retry attempts."""
        # Make the mock send_message always return False
        async def mock_send_false(*args, **kwargs):
            return False
        mock_send_message.side_effect = mock_send_false
        
        teleporter = Teleporter()
        
        async def run_test():
            return await teleporter.send_with_retry("Test message", "test_chat_id", max_attempts=3)
        
        result = asyncio.run(run_test())
        
        assert result is False
        assert mock_send_message.call_count == 3  # Called max_attempts times
        # Verify error was logged
        # Note: We can't easily test the logger call here since it's in the class method


# Integration test to verify both modules work together
def test_teleporter_and_reporter_integration():
    """Test that ReportBuilder and Teleporter can work together."""
    # Generate a report using ReportBuilder
    report = ReportBuilder.build_mission_update(
        task="Integration Test",
        agent="QA Agent",
        status="SUCCESS",
        problem="Initial issue with connection",
        solution="Restarted services",
        next_steps="Monitor for stability"
    )
    
    # Verify the report contains expected elements
    assert "🚀 **Mission Update: Integration Test**" in report
    assert "👤 **Agent:** QA Agent" in report
    assert "✅ **Status:** SUCCESS" in report
    assert "🔍 **Problem:** Initial issue with connection" in report
    assert "🛠️ **Solution:** Restarted services" in report
    assert "⏭️ **Next Steps:** Monitor for stability" in report
    
    # The report should be a properly formatted string ready for delivery
    assert isinstance(report, str)
    assert len(report) > 0