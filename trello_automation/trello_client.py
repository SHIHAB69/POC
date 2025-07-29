import requests
from typing import Dict, List, Optional
from dataclasses import dataclass
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@dataclass
class TrelloCardData:
    name: str
    description: str
    list_id: str
    labels: List[str] = None
    due_date: str = None
    members: List[str] = None

class TrelloClient:
    """Trello API client for card operations"""
    
    def __init__(self):
        self.api_key = settings.TRELLO_CONFIG['API_KEY']
        self.token = settings.TRELLO_CONFIG['TOKEN']
        self.board_id = settings.TRELLO_CONFIG['BOARD_ID']
        self.base_url = "https://api.trello.com/1"
        
    def _make_request(self, method: str, endpoint: str, params: Dict = None, data: Dict = None):
        """Make authenticated request to Trello API"""
        url = f"{self.base_url}{endpoint}"
        
        # Add authentication parameters
        auth_params = {
            'key': self.api_key,
            'token': self.token
        }
        
        if params:
            params.update(auth_params)
        else:
            params = auth_params
            
        try:
            response = requests.request(method, url, params=params, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Trello API request failed: {e}")
            raise
    
    def get_lists(self) -> List[Dict]:
        """Get all lists in the board"""
        return self._make_request('GET', f'/boards/{self.board_id}/lists')
    
    def get_labels(self) -> List[Dict]:
        """Get all labels in the board"""
        return self._make_request('GET', f'/boards/{self.board_id}/labels')
    
    def create_card(self, card_data: TrelloCardData) -> Dict:
        """Create a new card in Trello"""
        card_params = {
            'name': card_data.name,
            'desc': card_data.description,
            'idList': card_data.list_id,
        }
        
        if card_data.due_date:
            card_params['due'] = card_data.due_date
            
        if card_data.labels:
            # Get label IDs by names
            label_ids = self._get_label_ids_by_names(card_data.labels)
            if label_ids:
                card_params['idLabels'] = ','.join(label_ids)
        
        created_card = self._make_request('POST', '/cards', data=card_params)
        return created_card
    
    def _get_label_ids_by_names(self, label_names: List[str]) -> List[str]:
        """Get label IDs by names"""
        labels = self.get_labels()
        label_ids = []
        
        for label_name in label_names:
            for label in labels:
                if label['name'].lower() == label_name.lower():
                    label_ids.append(label['id'])
                    break
        
        return label_ids
    
    def get_list_id_by_name(self, list_name: str) -> Optional[str]:
        """Get list ID by name"""
        lists = self.get_lists()
        for list_item in lists:
            if list_item['name'].lower() == list_name.lower():
                return list_item['id']
        return None 