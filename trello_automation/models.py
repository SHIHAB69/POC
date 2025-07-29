from django.db import models
from django.utils import timezone

class TrelloCard(models.Model):
    """Model to track created Trello cards"""
    trello_card_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    list_name = models.CharField(max_length=100)
    labels = models.JSONField(default=list)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'trello_cards'

class AutomationLog(models.Model):
    """Model to track automation runs"""
    input_text = models.TextField()
    processed_data = models.JSONField()
    trello_card = models.ForeignKey(TrelloCard, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('success', 'Success'),
        ('error', 'Error'),
        ('pending', 'Pending')
    ])
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'automation_logs'
