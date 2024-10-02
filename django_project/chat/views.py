from django.http import HttpResponse
from django.utils import timezone

from django.shortcuts import render, redirect, reverse, get_object_or_404

from django.contrib.auth.decorators import login_required
from user.models import User
from form.models import Worksheet, Like
from .models import Chat, ChatUsers

# Create your views here.
@login_required
def index(request):
    this_worksheet, this_worksheet_created = Worksheet.objects.get_or_create(user=request.user)
    user = request.user

    if request.method == 'POST':
        other_user = get_object_or_404(User, pk=request.POST['user_id'])

        chat = Chat.objects.filter(users=user).filter(users=other_user).filter(is_group=False).first()

        if chat:
            # return HttpResponseRedirect(reverse('chat:room', kwargs={'chat_id': chat.id}))
            # Используйте reverse правильно с передачей chat_id
            return redirect(reverse('chat:room', kwargs={'chat_id': chat.id}))

        else:
            other_worksheet = get_object_or_404(Worksheet, user=other_user)
            like = Like.objects.filter(receiver=this_worksheet, sender=other_worksheet).first()

            if like:
                like.delete()
                new_chat = Chat(is_group=False)
                new_chat.save()

                datetime = timezone.now()

                ChatUsers.objects.create(user=user, chat=new_chat, date_joined=datetime, invite_reason='Создал чат.')

                ChatUsers.objects.create(user=other_user, chat=new_chat, date_joined=datetime,
                                         invite_reason='Был приглашен в чат.')

                return redirect(reverse('chat:room', kwargs={'chat_id': new_chat.id}))

            else:
                new_like, new_like_created = Like.objects.get_or_create(receiver=other_worksheet, sender=this_worksheet)
                if new_like_created:
                    new_like.save()

            worksheets = Worksheet.objects.exclude(pk=this_worksheet.id)

            chats = user.chats.all()

            context = {
                'worksheets': worksheets,
                'chats': chats,
                'title': 'Чаты',
            }

            return render(request, 'chat/index.html', context=context)

    else:

        worksheets = Worksheet.objects.exclude(pk=this_worksheet.id)

        chats = user.chats.all()

        context = {
            'worksheets': worksheets,
            'chats': chats,
            'title': 'Чаты',
        }

        return render(request, 'chat/index.html', context=context)



@login_required
def room(request, chat_id):

    chat = get_object_or_404(Chat, pk=chat_id)

    users = chat.users.all()

    # Если пользователь не является членом чата, его переносит на 'chat/'
    if not request.user in users:
        return redirect('chat:index')

    messages = chat.messages.all()

    context = {
        "chat_id": chat_id,
        "messages": messages,
    }

    return render(request, "chat/room.html", context=context)







