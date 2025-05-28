from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from .models import (
    Company, CompanyUser, Visitor, Conversation,
    Message, Ticket, ChatTrigger
)
from .forms import (
    MessageForm, TicketForm, ChatTriggerForm
)


@login_required
def conversation_list(request):
    # List all conversations in the user's company
    conversations = Conversation.objects.filter(company__companyuser__user=request.user)
    return render(request, 'chat/conversation_list.html', {'conversations': conversations})


@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    messages = conversation.message_set.order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.conversation = conversation
            msg.sender_type = 'agent'
            msg.sender_id = request.user.id
            msg.timestamp = timezone.now()
            msg.save()
            return redirect('conversation_detail', pk=conversation.pk)
    else:
        form = MessageForm()

    return render(request, 'chat/conversation_detail.html', {
        'conversation': conversation,
        'messages': messages,
        'form': form
    })


def start_conversation(request):
    # Called by the frontend visitor when initiating a chat session
    visitor = Visitor.objects.first()  # Replace with session logic

    # Create a new conversation
    conversation = Conversation.objects.create(
        visitor=visitor,
        company=visitor.company,
        assigned_agent=None,  # No agent assigned yet
        status='open',
        started_at=timezone.now()
    )

    # Auto-reply if no agent assigned (offline)
    Message.objects.create(
        conversation=conversation,
        sender_type='bot',
        sender_id=None,
        message="Thank you for reaching us. We'll be on it!",
        timestamp=timezone.now()
    )

    return redirect('conversation_detail', pk=conversation.pk)


def submit_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            # Example: Attach visitor/company based on session or form
            visitor = Visitor.objects.first()
            ticket.visitor = visitor
            ticket.company = visitor.company
            ticket.status = 'open'
            ticket.created_at = timezone.now()
            ticket.save()
            return redirect('ticket_thanks')
    else:
        form = TicketForm()

    return render(request, 'chat/submit_ticket.html', {'form': form})


def ticket_thanks(request):
    return render(request, 'chat/ticket_thanks.html')


def trigger_check(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    triggers = ChatTrigger.objects.filter(company=company, is_active=True)

    if triggers.exists():
        return JsonResponse({'message': triggers.first().message})
    return JsonResponse({'message': ''})


@login_required
def create_trigger(request):
    if request.method == 'POST':
        form = ChatTriggerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trigger_list')
    else:
        form = ChatTriggerForm()

    return render(request, 'chat/trigger_form.html', {'form': form})


@login_required
def trigger_list(request):
    triggers = ChatTrigger.objects.filter(company__companyuser__user=request.user)
    return render(request, 'chat/trigger_list.html', {'triggers': triggers})
