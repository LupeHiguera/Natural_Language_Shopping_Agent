"""
Test configuration and fixtures.
Ensures tests run in mock mode without requiring AWS credentials.
"""
import os
import sys

# Set mock mode BEFORE importing any app modules
# This must happen at the top of conftest.py before collection
os.environ["MOCK_MODE"] = "true"
os.environ["BEDROCK_AGENT_ID"] = ""
os.environ["BEDROCK_AGENT_ALIAS_ID"] = ""

# Force reload of config if already imported
if "app.config" in sys.modules:
    del sys.modules["app.config"]
if "app.main" in sys.modules:
    del sys.modules["app.main"]
