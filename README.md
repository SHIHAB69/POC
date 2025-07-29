# Northstar Recycling Trello Automation

AI-powered Trello automation system for Northstar Recycling's workflow management. This system automatically creates Trello cards from text input using AI processing and integrates with the Trello API.

## 🚀 Features

- **AI Text Processing**: Uses Gemini API to analyze text and extract structured data
- **Trello Integration**: Automatically creates cards with titles, descriptions, labels, and due dates
- **Fallback System**: Works even when AI API is unavailable
- **Database Logging**: Tracks all automation activities
- **REST API**: Full API endpoints for integration
- **LangGraph Integration**: Scalable workflow orchestration

## 🛠️ Technology Stack

- **Backend**: Django + Django REST Framework
- **AI**: Google Gemini API (with LangGraph integration)
- **Database**: SQLite (for POC, can be upgraded to PostgreSQL)
- **External APIs**: Trello API
- **Task Queue**: Celery + Redis (configured but not used in POC)

## 📋 Prerequisites

- Python 3.8+
- Trello API credentials
- Google Gemini API key

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd POC
   ```

2. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Configure settings**
   The API keys are configured in `northstar_automation/settings.py`. Update the following values:
   ```python
   TRELLO_CONFIG = {
       'API_KEY': 'your_trello_api_key',
       'TOKEN': 'your_trello_token',
       'BOARD_ID': 'your_board_id',
       'LIST_ID': 'your_list_id',
   }
   
   GEMINI_API_KEY = 'your_gemini_api_key'
   ```

4. **Run migrations**
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

5. **Start the server**
   ```bash
   python3 manage.py runserver 8000
   ```

## 🧪 Testing

### Quick Test
```bash
# Test connection
curl -X GET http://localhost:8000/api/trello/test-connection/

# Create a card
curl -X POST http://localhost:8000/api/trello/create-card/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here", "list_name": "To Do"}'
```

### Manual API Testing
```bash
# Test connection
curl -X GET http://localhost:8000/api/trello/test-connection/

# Create a card
curl -X POST http://localhost:8000/api/trello/create-card/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here", "list_name": "To Do"}'

# Get lists
curl -X GET http://localhost:8000/api/trello/lists/
```

## 🔌 API Endpoints

### POST `/api/trello/create-card/`
Create a Trello card from text input.

**Request:**
```json
{
  "text": "Your text description here",
  "list_name": "To Do"
}
```

**Response:**
```json
{
  "success": true,
  "card_id": "trello_card_id",
  "card_name": "Card Title",
  "card_url": "https://trello.com/c/card_url",
  "processed_data": {
    "title": "AI processed title",
    "description": "AI processed description",
    "labels": ["label1", "label2"],
    "due_date": "2024-01-15",
    "priority": "high"
  },
  "log_id": 123
}
```

### GET `/api/trello/test-connection/`
Test Trello API connection.

### GET `/api/trello/lists/`
Get all lists in the Trello board.

### GET `/api/trello/labels/`
Get all labels in the Trello board.

## 🤖 AI Processing

The system uses Google Gemini API to process text and extract:
- **Card Title**: Concise, descriptive title
- **Description**: Detailed information
- **Labels**: Relevant categories and priorities
- **Due Date**: Extracted dates (if mentioned)
- **Priority**: High/Medium/Low (if mentioned)

### Fallback System
When AI processing fails (rate limits, API errors), the system falls back to:
- Using the original text as title and description
- Setting default priority as "medium"
- Creating basic labels

## 📊 Database Models

### TrelloCard
Tracks created Trello cards:
- `trello_card_id`: Trello's card ID
- `name`: Card title
- `description`: Card description
- `list_name`: Target list name
- `labels`: JSON array of labels
- `due_date`: Due date (if set)
- `created_at`, `updated_at`: Timestamps

### AutomationLog
Tracks automation runs:
- `input_text`: Original input text
- `processed_data`: AI processed data (JSON)
- `trello_card`: Foreign key to TrelloCard
- `status`: Success/Error/Pending
- `error_message`: Error details (if any)
- `created_at`: Timestamp

## 🔄 Workflow

1. **Text Input**: User provides text description
2. **AI Processing**: Gemini API analyzes and extracts structured data
3. **Data Validation**: System validates and cleans extracted data
4. **Trello Creation**: Creates card in specified Trello list
5. **Database Logging**: Records the entire process
6. **Response**: Returns card details and processing results

## 🎯 Use Cases

### Northstar Recycling Workflow
- **Service Requests**: Automatically create task cards from email content
- **Supplier Research**: Generate research tasks with contact information
- **Delivery Coordination**: Create scheduling tasks with deadlines
- **Data Collection**: Track data entry and validation tasks

### Example Inputs
```
"Urgent: New supplier ABC Recycling needs profile research. Contact: john@abc.com. Deadline: Jan 25"
"Service request from XYZ Corp - Paper waste recycling, 3000 lbs, delivery by Jan 30"
"Metal recycling request from DEF Industries. Quantity: 1500 lbs. Contact: sarah@def.com"
```

## 🚀 Next Steps

1. **Outlook Integration**: Email processing and automation
2. **CieTrade Integration**: Transaction management
3. **Quip Integration**: Document management
4. **Chatbot Interface**: User interaction layer
5. **Advanced AI Features**: Predictive analytics, risk assessment

## 📝 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Google Gemini API key
- `TRELLO_API_KEY`: Trello API key
- `TRELLO_TOKEN`: Trello access token
- `TRELLO_BOARD_ID`: Target Trello board ID
- `TRELLO_LIST_ID`: Default list ID for new cards

### Trello Setup
1. Get API key from: https://trello.com/app-key
2. Generate token by clicking "Token" link
3. Get board ID from board URL
4. Get list ID using the test-connection endpoint

## 🐛 Troubleshooting

### Common Issues
1. **Gemini API Rate Limits**: System falls back to basic processing
2. **Trello Authentication**: Check API key and token
3. **List Not Found**: Verify list name and board access
4. **Database Errors**: Run migrations and check SQLite permissions

### Debug Mode
Set `DEBUG=True` in config.env for detailed error messages.

## 📄 License

This project is part of the Northstar Recycling POC and is confidential.

## 🤝 Support

For issues and questions, contact the development team. 