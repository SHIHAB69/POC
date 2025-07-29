import google.generativeai as genai
from typing import Dict, Any, List
from django.conf import settings
import json
import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

class AITextProcessor:
    """AI processor using Gemini for text analysis"""
    
    def __init__(self):
        self.model = model
    
    def process_text(self, text: str) -> Dict[str, Any]:
        """Process text and return structured data for Trello card"""
        try:
            prompt = f"""
            Analyze the following text and extract information for creating a Trello card.
            Return a JSON object with the following structure:
            {{
                "title": "Concise, descriptive card title (max 100 characters)",
                "description": "Detailed description with all relevant information",
                "labels": ["label1", "label2"],
                "due_date": "YYYY-MM-DD (if mentioned, otherwise null)",
                "priority": "high/medium/low (if mentioned, otherwise medium)"
            }}
            
            Text to analyze: {text}
            
            JSON Response:
            """
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                extracted_data = json.loads(json_match.group())
            else:
                raise Exception("No valid JSON found in response")
            
            # Validate and clean extracted data
            extracted_data = self._validate_data(extracted_data, text)
            
            return extracted_data
            
        except Exception as e:
            logger.error(f"Error processing text with AI: {e}")
            # Return fallback data
            return self._create_fallback_data(text)
    
    def _validate_data(self, data: Dict[str, Any], original_text: str) -> Dict[str, Any]:
        """Validate and clean extracted data"""
        # Ensure required fields
        if not data.get('title'):
            data['title'] = original_text[:100] + "..." if len(original_text) > 100 else original_text
            
        if not data.get('description'):
            data['description'] = original_text
            
        if not data.get('labels'):
            data['labels'] = []
            
        if not data.get('priority'):
            data['priority'] = 'medium'
            
        if not data.get('due_date'):
            data['due_date'] = None
        
        # Clean up labels
        if data.get('labels'):
            # Add priority as label
            priority = data.get('priority', 'medium')
            if priority not in data['labels']:
                data['labels'].append(priority)
        
        return data
    
    def _create_fallback_data(self, text: str) -> Dict[str, Any]:
        """Create fallback data when AI processing fails"""
        return {
            "title": text[:100] + "..." if len(text) > 100 else text,
            "description": text,
            "labels": ["medium"],
            "due_date": None,
            "priority": "medium"
        } 