from django.shortcuts import render
from .models import ChatRoom, Message
from account.models import Site, CustomSession
from django.shortcuts import get_object_or_404

def index(request):
    print(request.session)
    request.session.save()

    return render(request, 'chat/index.html', { 'session_key': request.session.session_key})
    
def room(request):
    if request.method == 'GET':
        request.session.save()
        session_key = request.session.session_key
        
        if not request.user.is_staff:
            if not ChatRoom.objects.filter(session=session_key).exists():
                domain_name = request.META['HTTP_HOST'].split(':')[0]
                custom_session = CustomSession.objects.get(session_key=session_key)
                site = Site.objects.filter(url=f'http://{domain_name}').first()
                admin_user = site.profile.user
                # domain_name = request.META['HTTP_HOST']
                print('domain_name_from_view %s' % domain_name)
                # admin_user = Site.objects.get(url=f'http://{domain_name}').profile.user
        
                ChatRoom.objects.create(session=custom_session, 
                                         admin_user=admin_user,
                                         site=site,
                                         name=admin_user
                                       )
            try:
                chat_id = get_object_or_404(ChatRoom, session=session_key).id
                messages = list(Message.objects.filter(chat_room=chat_id))
            
            except:
                messages = None
            
                
            
    print('messages== ', messages)
    return render (request, 'chat/chatroom.html', {'messages': messages})

def chat_list(request):
    if request.method == 'GET':
        chat_list = None
        if request.user.is_staff:
            # domain_name = request.META['HTTP_HOST'].split(':')[0]
            domain_name = request.user.domain_name
            print(domain_name)
            chat_list = list(ChatRoom.objects.filter(site=f'http://{domain_name}'))
            
    return render(request, 'chat/index.html', {'chat_list': chat_list})

def answer_to_chat(request, room_name):
    try:
        chat_id = get_object_or_404(ChatRoom, unique_code=room_name).id
        messages = list(Message.objects.filter(chat_room=chat_id))
        
    except:
        messages = None
    
    return render(request, 'chat/admin_chatroom.html', {'room_name': room_name, 'messages': messages})