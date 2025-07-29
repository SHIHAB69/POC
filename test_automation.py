#!/usr/bin/env python3
"""
Test script for Northstar Recycling Trello Automation
Demonstrates AI-powered text processing and Trello card creation
"""

import os
import sys
import django
import json
import requests

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'northstar_automation.settings')
django.setup()

from trello_automation.automation_service import TrelloAutomationService

def test_trello_automation():
    """Test the complete Trello automation workflow"""
    
    print("🚀 Northstar Recycling Trello Automation Test")
    print("=" * 50)
    
    # Initialize service
    service = TrelloAutomationService()
    
    # Test 1: Connection
    print("\n1. Testing Trello API Connection...")
    connection_result = service.test_connection()
    if connection_result['success']:
        print(f"✅ {connection_result['message']}")
    else:
        print(f"❌ Connection failed: {connection_result['error']}")
        return
    
    # Test 2: Create card from text
    test_texts = [
        "Urgent: New supplier XYZ Recycling needs profile research. Contact: john@xyz.com. Deadline: Jan 20",
        "Service request from ABC Corp - Paper waste, 5000 lbs, delivery by Jan 15",
        "High priority: Metal recycling request from DEF Industries. Quantity: 2000 lbs. Contact: mike@def.com"
    ]
    
    print("\n2. Testing AI Text Processing and Card Creation...")
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n   Test {i}: Processing text...")
        print(f"   Input: {text[:50]}...")
        
        result = service.create_card_from_text(text)
        
        if result['success']:
            print(f"   ✅ Card created successfully!")
            print(f"   📋 Card ID: {result['card_id']}")
            print(f"   📝 Card Name: {result['card_name']}")
            print(f"   🔗 Card URL: {result['card_url']}")
            
            # Show processed data
            processed = result['processed_data']
            print(f"   🤖 AI Processed Data:")
            print(f"      - Title: {processed.get('title', 'N/A')}")
            print(f"      - Priority: {processed.get('priority', 'N/A')}")
            print(f"      - Labels: {processed.get('labels', [])}")
            print(f"      - Due Date: {processed.get('due_date', 'N/A')}")
        else:
            print(f"   ❌ Failed to create card: {result['error']}")
    
    # Test 3: API Endpoint (if server is running)
    print("\n3. Testing API Endpoint...")
    try:
        response = requests.post(
            'http://localhost:8000/api/trello/create-card/',
            json={
                'text': 'API Test: New recycling request from GHI Corp. Contact: api@ghi.com',
                'list_name': 'To Do'
            },
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            data = response.json()
            print(f"   ✅ API call successful!")
            print(f"   📋 Card ID: {data['card_id']}")
            print(f"   🔗 Card URL: {data['card_url']}")
        else:
            print(f"   ❌ API call failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print("   ⚠️  Server not running. Start with: python manage.py runserver 8000")
    
    print("\n" + "=" * 50)
    print("🎉 Test completed!")
    print("\nNext steps:")
    print("1. Check your Trello board to see the created cards")
    print("2. Start the server: python manage.py runserver 8000")
    print("3. Use the API endpoint for integration")

if __name__ == "__main__":
    test_trello_automation() 