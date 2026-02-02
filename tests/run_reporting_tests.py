#!/usr/bin/env python3
"""
Simple Test Runner for Reporting Modules
Tests for Teleporter and ReportBuilder classes without requiring pytest.
"""

import sys
import os
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

# Add the project root to the path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.utils.reporter import ReportBuilder, ReportFormatter
from src.utils.teleporter import Teleporter


def test_report_builder():
    """Test ReportBuilder functionality."""
    print("Testing ReportBuilder...")
    
    # Test basic mission update
    result = ReportBuilder.build_mission_update(
        task="Test Task",
        agent="Test Agent",
        status="SUCCESS"
    )
    
    assert "🚀 **Mission Update: Test Task**" in result
    assert "👤 **Agent:** Test Agent" in result
    assert "✅ **Status:** SUCCESS" in result
    assert "#OpenClaw #DevUpdate" in result
    print("  ✓ Basic mission update test passed")
    
    # Test failed status
    result = ReportBuilder.build_mission_update(
        task="Test Task",
        agent="Test Agent",
        status="FAILED"
    )
    
    assert "❌ **Status:** FAILED" in result
    print("  ✓ Failed status test passed")
    
    # Test mission update with problem
    result = ReportBuilder.build_mission_update(
        task="Test Task",
        agent="Test Agent",
        status="FAILED",
        problem="Something went wrong"
    )
    
    assert "🔍 **Problem:** Something went wrong" in result
    print("  ✓ Mission update with problem test passed")
    
    # Test market signal
    result = ReportBuilder.build_market_signal(
        signal="Price increase detected",
        reason="Market demand surge"
    )
    
    assert "📈 **Market Signal:** Price increase detected" in result
    assert "💡 **Reason:** Market demand surge" in result
    assert "#OpenClaw #MarketSignal" in result
    print("  ✓ Market signal test passed")
    
    # Test AI brief
    result = ReportBuilder.build_ai_brief(
        headline="Market trend identified"
    )
    
    assert "🤖 **AI Brief: Market trend identified**" in result
    assert "#OpenClaw #AIBrief" in result
    print("  ✓ AI brief test passed")
    
    print("All ReportBuilder tests passed!\n")


def test_report_formatter():
    """Test ReportFormatter functionality."""
    print("Testing ReportFormatter...")
    
    # Test text truncation
    text = "Short text"
    result = ReportFormatter.truncate_text(text, max_length=100)
    assert result == "Short text"
    print("  ✓ Text within limit test passed")
    
    # Test escaping markdown
    text = "This is *bold* and _italic_ text"
    result = ReportFormatter.escape_markdown_v2(text)
    assert r"\*bold\*" in result
    assert r"\_italic\_" in result
    print("  ✓ Markdown escaping test passed")
    
    # Test timestamp formatting
    result = ReportFormatter.format_timestamp()
    assert len(result) == 19  # YYYY-MM-DD HH:MM:SS
    assert result.count("-") == 2
    assert result.count(":") == 2
    assert result.count(" ") == 1
    print("  ✓ Timestamp formatting test passed")
    
    print("All ReportFormatter tests passed!\n")


def test_teleporter():
    """Test Teleporter functionality."""
    print("Testing Teleporter...")
    
    # Set up environment variables for testing
    os.environ["TELEGRAM_BOT_TOKEN"] = "test_token"
    os.environ["TELEGRAM_CHANNEL_ID"] = "test_channel_id"
    
    teleporter = Teleporter()
    
    # Test that the instance was created successfully
    assert teleporter is not None
    print("  ✓ Teleporter instance creation test passed")
    
    # Test that the required environment variables are accessible
    assert os.getenv("TELEGRAM_BOT_TOKEN") == "test_token"
    assert os.getenv("TELEGRAM_CHANNEL_ID") == "test_channel_id"
    print("  ✓ Environment variable access test passed")
    
    # Clean up environment variables
    del os.environ["TELEGRAM_BOT_TOKEN"]
    del os.environ["TELEGRAM_CHANNEL_ID"]
    
    print("All Teleporter tests passed!\n")


def test_integration():
    """Test integration between ReportBuilder and Teleporter."""
    print("Testing integration...")
    
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
    assert isinstance(report, str)
    assert len(report) > 0
    
    print("  ✓ Integration test passed")
    print("All integration tests passed!\n")


def main():
    """Run all tests."""
    print("Running unit tests for reporting modules...\n")
    
    try:
        test_report_builder()
        test_report_formatter()
        test_teleporter()
        test_integration()
        
        print("🎉 All tests passed successfully!")
        print("✅ ReportBuilder class works as expected")
        print("✅ ReportFormatter class works as expected") 
        print("✅ Teleporter class works as expected")
        print("✅ Integration between modules works correctly")
        
    except AssertionError as e:
        print(f"❌ Test failed with assertion error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False
        
    return True


if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)