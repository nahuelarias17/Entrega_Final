from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Message
from .forms import ComposeForm

@login_required
def home(request):
    messages = Message.objects.all()
    return render(request, 'home.html', {'messages': messages})


@login_required
def inbox_view(request):
    messages = Message.objects.filter(recipient=request.user).order_by('-sent_at')
    paginator = Paginator(messages, 5)
    page = request.GET.get('page')
    messages = paginator.get_page(page)
    return render(request, 'blog_messages/inbox.html', {'messages': messages})


@login_required
def outbox_view(request):
    messages = Message.objects.filter(sender=request.user).order_by('-sent_at')
    paginator = Paginator(messages, 5)
    page = request.GET.get('page')
    messages = paginator.get_page(page)
    return render(request, 'blog_messages/outbox.html', {'messages': messages})


@login_required
def send_message_view(request):
    if request.method == 'POST':
        form = ComposeForm(request.POST)
        if form.is_valid():
            recipient = form.cleaned_data.get('recipient')
            subject = form.cleaned_data.get('subject')
            body = form.cleaned_data.get('body')
            if body:
                message = Message(sender=request.user, recipient=recipient, subject=subject, body=body)
                message.save()
                messages.success(request, 'Mensaje enviado')
                return redirect('blog_messages:inbox')
            else:
                messages.error(request, 'El mensaje no puede estar vacío')
        else:
            messages.error(request, 'Por favor corregí los errores del formulario')
    else:
        form = ComposeForm()
    return render(request, 'blog_messages/send.html', {'form': form})



@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.recipient == request.user or message.sender == request.user:
        return render(request, 'blog_messages/views.html', {'message': message})
    else:
        messages.error(request, 'No tenés permiso para ver este mensaje')
        return redirect('blog_messages:inbox')


@login_required
def reply_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.method == 'POST':
        form = ComposeForm(request.POST)
        if form.is_valid():
            sender = request.user
            recipient = message.sender
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            reply_message = Message.objects.create(sender=sender, recipient=recipient, subject=subject, body=body,
                                                   parent_message=message)
            reply_message.save()
            messages.success(request, f'Reply sent to {message.sender.username}!')
            return redirect('blog_messages:inbox')
    else:
        initial_data = {
            'subject': f"Re: {message.subject}",
            'body': f"\n\n\n------ Original Message ------\nFrom: {message.sender}\nSubject: {message.subject}\n{message.body}"
        }
        form = ComposeForm(initial=initial_data)
    return render(request, 'blog_messages/reply_message.html', {'form': form})

def messages_section(request):
    return render(request, 'blog_messages/messages_section.html')
