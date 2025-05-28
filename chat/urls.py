from django.urls import path
from . import views

urlpatterns = [
    # Conversation views
    path('conversations/', views.conversation_list, name='conversation_list'),
    path('conversations/<uuid:pk>/', views.conversation_detail, name='conversation_detail'),
    path('conversations/start/', views.start_conversation, name='start_conversation'),

    # Ticket views
    path('ticket/submit/', views.submit_ticket, name='submit_ticket'),
    path('ticket/thanks/', views.ticket_thanks, name='ticket_thanks'),

    # Trigger views
    path('trigger/<uuid:company_id>/', views.trigger_check, name='trigger_check'),
    path('trigger/create/', views.create_trigger, name='create_trigger'),
    path('trigger/list/', views.trigger_list, name='trigger_list'),
]
