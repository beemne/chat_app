import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('agent', 'Agent'),
        ('company_admin', 'Company Admin'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=128)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Company(models.Model):
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField()
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)


class CompanyUser(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('agent', 'Agent'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(default=timezone.now)


class Visitor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    location = models.CharField(max_length=255)
    first_seen = models.DateTimeField(default=timezone.now)
    last_seen = models.DateTimeField(default=timezone.now)


class Conversation(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    assigned_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True, blank=True)


class Message(models.Model):
    SENDER_CHOICES = [
        ('visitor', 'Visitor'),
        ('agent', 'Agent'),
        ('bot', 'Bot'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender_type = models.CharField(max_length=10, choices=SENDER_CHOICES)
    sender_id = models.UUIDField()
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('pending', 'Pending'),
        ('closed', 'Closed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    assigned_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    resolved_at = models.DateTimeField(null=True, blank=True)


class ChatTrigger(models.Model):
    CONDITION_CHOICES = [
        ('time_on_page', 'Time on Page'),
        ('first_visit', 'First Visit'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    condition_type = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    condition_value = models.CharField(max_length=255)
    message = models.TextField()
    is_active = models.BooleanField(default=True)


class ChatAnalytics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    response_time = models.IntegerField()
    duration = models.IntegerField()
    rating = models.IntegerField()
