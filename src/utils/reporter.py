#!/usr/bin/env python3
"""
Reporter Module - Report Formatting Classes
Handles the formatting and content structure for various types of reports.
"""

from typing import Dict, List, Optional
from datetime import datetime


class ReportBuilder:
    """Handles the formatting and content structure for reports."""
    
    @staticmethod
    def build_mission_update(
        task: str,
        agent: str,
        status: str,
        problem: Optional[str] = None,
        solution: Optional[str] = None,
        next_steps: Optional[str] = None,
        report: Optional[str] = None
    ) -> str:
        """
        Build a mission update report.
        
        Args:
            task: Task ID or Name
            agent: Agent Role Name
            status: Status of the task
            problem: Problem encountered
            solution: Solution applied
            next_steps: Next steps planned
            report: Additional report content
            
        Returns:
            Formatted Markdown string
        """
        # Determine emoji based on status
        status_emoji = "✅" if status.upper() == "SUCCESS" else "❌"
        
        # Construct the message based on available fields
        template = f"🚀 **Mission Update: {task}**\n\n"
        template += f"👤 **Agent:** {agent}\n"
        template += f"{status_emoji} **Status:** {status}\n\n"
        
        if problem:
            template += f"🔍 **Problem:** {problem}\n\n"
        if solution:
            template += f"🛠️ **Solution:** {solution}\n\n"
        if next_steps:
            template += f"⏭️ **Next Steps:** {next_steps}\n\n"
        if report:
            template += f"📋 **Report:** {report}\n\n"
        
        template += f"#OpenClaw #DevUpdate"
        return template

    @staticmethod
    def build_market_signal(
        signal: str,
        reason: str,
        audit: Optional[str] = None
    ) -> str:
        """
        Build a market signal report.
        
        Args:
            signal: The market signal detected
            reason: Reason for the signal
            audit: Audit trail or additional information
            
        Returns:
            Formatted Markdown string
        """
        template = f"📈 **Market Signal:** {signal}\n\n"
        template += f"💡 **Reason:** {reason}\n\n"
        
        if audit:
            template += f"🔍 **Audit Trail:** {audit}\n\n"
        
        template += f"#OpenClaw #MarketSignal"
        return template

    @staticmethod
    def build_ai_brief(
        headline: str,
        deep_dive: Optional[str] = None,
        kol_sentiment: Optional[str] = None,
        system_audit: Optional[str] = None
    ) -> str:
        """
        Build an AI brief report.
        
        Args:
            headline: Main headline or summary
            deep_dive: Detailed analysis
            kol_sentiment: Sentiment from Key Opinion Leaders
            system_audit: System audit information
            
        Returns:
            Formatted Markdown string
        """
        template = f"🤖 **AI Brief: {headline}**\n\n"
        
        if deep_dive:
            template += f"🔬 **Deep Dive:** {deep_dive}\n\n"
        if kol_sentiment:
            template += f"💬 **KOL Sentiment:** {kol_sentiment}\n\n"
        if system_audit:
            template += f"⚙️ **System Audit:** {system_audit}\n\n"
        
        template += f"#OpenClaw #AIBrief"
        return template


class ReportFormatter:
    """Additional utilities for report formatting and manipulation."""
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 4000) -> str:
        """
        Truncate text to fit within Telegram's message limits.
        
        Args:
            text: Text to truncate
            max_length: Maximum allowed length
            
        Returns:
            Truncated text with indicator if truncated
        """
        if len(text) <= max_length:
            return text
        
        truncation_indicator = "\n\n...(truncated)"
        available_space = max_length - len(truncation_indicator)
        
        return text[:available_space] + truncation_indicator

    @staticmethod
    def format_timestamp(timestamp: Optional[datetime] = None) -> str:
        """
        Format timestamp for reports.
        
        Args:
            timestamp: Optional datetime object, defaults to now
            
        Returns:
            Formatted timestamp string
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def escape_markdown_v2(text: str) -> str:
        """
        Escape special characters for Telegram MarkdownV2.
        
        Args:
            text: Text to escape
            
        Returns:
            Escaped text
        """
        # Characters to escape in Telegram MarkdownV2
        chars_to_escape = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        
        for char in chars_to_escape:
            text = text.replace(char, f'\\{char}')
        
        return text