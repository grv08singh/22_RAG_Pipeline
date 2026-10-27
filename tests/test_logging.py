"""
Tests for the logging utility module.
"""

import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.logging import setup_logging, get_logger


def test_setup_logging():
    """Test that setup_logging configures the root logger."""
    logger = setup_logging(level=logging.DEBUG)
    assert logger.level == logging.DEBUG
    assert len(logger.handlers) >= 1


def test_get_logger():
    """Test that get_logger returns a logger instance."""
    logger = get_logger("test_module")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_module"


def test_logging_output(capsys):
    """Test that logging produces output."""
    setup_logging(level=logging.INFO)
    logger = get_logger("test_output")
    logger.info("Test message")
    captured = capsys.readouterr()
    assert "Test message" in captured.out