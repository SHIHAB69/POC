from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .automation_service import TrelloAutomationService
import json
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST"])
def create_card_from_text(request):
    """API endpoint to create Trello card from text input"""
    try:
        data = json.loads(request.body)
        text_input = data.get('text')
        list_name = data.get('list_name', 'To Do')
        
        if not text_input:
            return JsonResponse({
                'success': False,
                'error': 'text field is required'
            }, status=400)
        
        # Create automation service
        service = TrelloAutomationService()
        
        # Create card
        result = service.create_card_from_text(text_input, list_name)
        
        if result['success']:
            return JsonResponse(result, status=201)
        else:
            return JsonResponse(result, status=500)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON'
        }, status=400)
    except Exception as e:
        logger.error(f"Error in create_card_from_text: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def test_connection(request):
    """Test Trello API connection"""
    try:
        service = TrelloAutomationService()
        result = service.test_connection()
        
        if result['success']:
            return JsonResponse(result, status=200)
        else:
            return JsonResponse(result, status=500)
            
    except Exception as e:
        logger.error(f"Error in test_connection: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def get_board_lists(request):
    """Get all lists in the Trello board"""
    try:
        service = TrelloAutomationService()
        lists = service.get_board_lists()
        
        return JsonResponse({
            'success': True,
            'lists': lists
        }, status=200)
        
    except Exception as e:
        logger.error(f"Error in get_board_lists: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def get_board_labels(request):
    """Get all labels in the Trello board"""
    try:
        service = TrelloAutomationService()
        labels = service.get_board_labels()
        
        return JsonResponse({
            'success': True,
            'labels': labels
        }, status=200)
        
    except Exception as e:
        logger.error(f"Error in get_board_labels: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
