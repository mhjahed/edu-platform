from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User

@login_required
def inbox(request):
    messages = Message.objects.filter(receiver=request.user).order_by('-sent_at')
    return render(request, 'messaging/inbox.html', {'messages': messages})

@login_required
def send_message(request):
    reply_to = request.GET.get('reply_to')
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver')
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        receiver = get_object_or_404(User, id=receiver_id)
        Message.objects.create(sender=request.user, receiver=receiver, subject=subject, body=body)
        return redirect('inbox')
    if reply_to:
        users = User.objects.filter(id=reply_to)
    elif request.user.profile.role == 'Candidate':
        users = User.objects.filter(profile__role='Examiner')
    else:
        users = User.objects.filter(profile__role='Candidate')
    return render(request, 'messaging/send_message.html', {'users': users, 'reply_to': reply_to})

@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.is_read = True
    message.save()
    return render(request, 'messaging/view_message.html', {'message': message})
