#!/usr/bin/env python3
"""
Startup script for Northstar Recycling Trello Automation Server
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def start_server():
    """Start the Django development server"""
    
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'northstar_automation.settings')
    django.setup()
    
    print("🚀 Starting Northstar Recycling Trello Automation Server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("🔗 API Endpoints:")
    print("   - POST /api/trello/create-card/ - Create card from text")
    print("   - GET  /api/trello/test-connection/ - Test connection")
    print("   - GET  /api/trello/lists/ - Get board lists")
    print("   - GET  /api/trello/labels/ - Get board labels")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Start the server
    execute_from_command_line(['manage.py', 'runserver', '8000'])

if __name__ == "__main__":
    start_server() 