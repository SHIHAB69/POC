from django.urls import path
from . import views

urlpatterns = [
    path('api/trello/create-card/', views.create_card_from_text, name='create_card_from_text'),
    path('api/trello/test-connection/', views.test_connection, name='test_connection'),
    path('api/trello/lists/', views.get_board_lists, name='get_board_lists'),
    path('api/trello/labels/', views.get_board_labels, name='get_board_labels'),
] 