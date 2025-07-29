from .ai_processor import AITextProcessor
from .trello_client import TrelloClient, TrelloCardData
from .models import TrelloCard, AutomationLog
from django.conf import settings
import logging
from datetime import datetime
from typing import Dict, List

logger = logging.getLogger(__name__)

class TrelloAutomationService:
    """Main service for Trello automation with AI text processing"""
    
    def __init__(self):
        self.ai_processor = AITextProcessor()
        self.trello_client = TrelloClient()
        
    def create_card_from_text(self, text: str, list_name: str = "To Do") -> Dict:
        """Create a Trello card from text input using AI processing"""
        
        # Create automation log entry
        log_entry = AutomationLog.objects.create(
            input_text=text,
            processed_data={},
            status='pending'
        )
        
        try:
            # Step 1: Process text with AI
            logger.info(f"Processing text with AI: {text[:50]}...")
            processed_data = self.ai_processor.process_text(text)
            
            # Update log with processed data
            log_entry.processed_data = processed_data
            log_entry.save()
            
            # Step 2: Get list ID
            list_id = self.trello_client.get_list_id_by_name(list_name)
            if not list_id:
                raise Exception(f"List '{list_name}' not found in Trello board")
            
            # Step 3: Create Trello card data
            card_data = TrelloCardData(
                name=processed_data['title'],
                description=processed_data['description'],
                list_id=list_id,
                labels=processed_data.get('labels', []),
                due_date=processed_data.get('due_date')
            )
            
            # Step 4: Create card in Trello
            logger.info(f"Creating Trello card: {card_data.name}")
            created_card = self.trello_client.create_card(card_data)
            
            # Step 5: Save to database
            trello_card = TrelloCard.objects.create(
                trello_card_id=created_card['id'],
                name=created_card['name'],
                description=created_card.get('desc', ''),
                list_name=list_name,
                labels=processed_data.get('labels', []),
                due_date=processed_data.get('due_date')
            )
            
            # Update log with success
            log_entry.trello_card = trello_card
            log_entry.status = 'success'
            log_entry.save()
            
            logger.info(f"Successfully created Trello card: {created_card['id']}")
            
            return {
                'success': True,
                'card_id': created_card['id'],
                'card_name': created_card['name'],
                'card_url': created_card['url'],
                'processed_data': processed_data,
                'log_id': log_entry.id
            }
            
        except Exception as e:
            logger.error(f"Error creating Trello card: {e}")
            
            # Update log with error
            log_entry.status = 'error'
            log_entry.error_message = str(e)
            log_entry.save()
            
            return {
                'success': False,
                'error': str(e),
                'log_id': log_entry.id
            }
    
    def get_board_lists(self) -> List[Dict]:
        """Get all lists in the Trello board"""
        try:
            return self.trello_client.get_lists()
        except Exception as e:
            logger.error(f"Error getting board lists: {e}")
            return []
    
    def get_board_labels(self) -> List[Dict]:
        """Get all labels in the Trello board"""
        try:
            return self.trello_client.get_labels()
        except Exception as e:
            logger.error(f"Error getting board labels: {e}")
            return []
    
    def test_connection(self) -> Dict:
        """Test Trello API connection"""
        try:
            lists = self.trello_client.get_lists()
            return {
                'success': True,
                'message': f"Connected successfully. Found {len(lists)} lists.",
                'lists': [{'id': l['id'], 'name': l['name']} for l in lists]
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            } 