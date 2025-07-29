from django.core.management.base import BaseCommand
from trello_automation.automation_service import TrelloAutomationService
import json

class Command(BaseCommand):
    help = 'Test Trello automation with AI text processing'

    def add_arguments(self, parser):
        parser.add_argument('--text', type=str, help='Text to process and create card from')
        parser.add_argument('--test-connection', action='store_true', help='Test Trello API connection')
        parser.add_argument('--get-lists', action='store_true', help='Get all lists in the board')

    def handle(self, *args, **options):
        service = TrelloAutomationService()
        
        if options['test_connection']:
            self.stdout.write('Testing Trello API connection...')
            result = service.test_connection()
            if result['success']:
                self.stdout.write(self.style.SUCCESS(f"✅ {result['message']}"))
                for list_info in result['lists']:
                    self.stdout.write(f"  - {list_info['name']} (ID: {list_info['id']})")
            else:
                self.stdout.write(self.style.ERROR(f"❌ Connection failed: {result['error']}"))
            return
        
        if options['get_lists']:
            self.stdout.write('Getting board lists...')
            lists = service.get_board_lists()
            for list_item in lists:
                self.stdout.write(f"  - {list_item['name']} (ID: {list_item['id']})")
            return
        
        if options['text']:
            self.stdout.write(f'Processing text: "{options["text"]}"')
            result = service.create_card_from_text(options['text'])
            
            if result['success']:
                self.stdout.write(self.style.SUCCESS('✅ Card created successfully!'))
                self.stdout.write(f"  Card ID: {result['card_id']}")
                self.stdout.write(f"  Card Name: {result['card_name']}")
                self.stdout.write(f"  Card URL: {result['card_url']}")
                self.stdout.write(f"  Processed Data: {json.dumps(result['processed_data'], indent=2)}")
            else:
                self.stdout.write(self.style.ERROR(f"❌ Failed to create card: {result['error']}"))
            return
        
        # Default: show help
        self.stdout.write('No action specified. Use --help for options.')
        self.stdout.write('Example usage:')
        self.stdout.write('  python manage.py test_trello_automation --test-connection')
        self.stdout.write('  python manage.py test_trello_automation --get-lists')
        self.stdout.write('  python manage.py test_trello_automation --text "New service request from ABC Corp"') 