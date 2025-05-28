from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (
    User, Company, CompanyUser, Visitor,
    Message, Ticket, ChatTrigger
)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'role', 'password1', 'password2']


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'industry', 'website', 'plan']


class CompanyUserForm(forms.ModelForm):
    class Meta:
        model = CompanyUser
        fields = ['user', 'company', 'role', 'is_active']


class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = [
            'company', 'session_id', 'ip_address',
            'user_agent', 'location', 'first_seen', 'last_seen'
        ]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'message']


class ChatTriggerForm(forms.ModelForm):
    class Meta:
        model = ChatTrigger
        fields = ['company', 'condition_type', 'condition_value', 'message', 'is_active']
