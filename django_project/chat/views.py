from django.utils import timezone

from django.shortcuts import render, redirect, reverse, get_object_or_404

from django.contrib.auth.decorators import login_required
from user.models import User
from .models import Chat, ChatUsers

# Create your views here.

def index(request):

    if request.method == 'POST':
        other_user = get_object_or_404(User, pk=request.POST['user_id'])
        user = request.user

        chat = Chat.objects.filter(users=user).filter(users=other_user).filter(is_group=False).first()

        if chat:
            # return HttpResponseRedirect(reverse('chat:room', kwargs={'chat_id': chat.id}))
            # Используйте reverse правильно с передачей chat_id
            return redirect(reverse('chat:room', kwargs={'chat_id': chat.id}))

        else:
            new_chat = Chat(is_group=False)
            new_chat.save()

            datetime = timezone.now()

            ChatUsers.objects.create(user=user, chat=new_chat, date_joined=datetime, invite_reason='Создал чат.')

            ChatUsers.objects.create(user=other_user, chat=new_chat, date_joined=datetime,
                                     invite_reason='Был приглашен в чат.')

            return redirect(reverse('chat:room', kwargs={'chat_id': new_chat.id}))

    else:
        users = User.objects.exclude(pk=request.user.id)

        context = {
            'users': users,
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

    context = {
        "chat_id": chat_id,
    }

    return render(request, "chat/room.html", context=context)







