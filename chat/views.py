from django.shortcuts import render
from .models import GroupChat
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import re
import codecs

def index(request):
    print(request.session)
    request.session.save()

    return render(request, 'chat/index.html', { 'session_key': request.session.session_key})
    
    
def aes_encryption(s1, s2):
    combined_string = s1 + s2
    encryption_key = get_random_bytes(16)
    cipher = AES.new(encryption_key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(combined_string.encode())
    # print(type(ciphertext))
    ciphertext = ciphertext.decode('latin-1')
    # print('ciphertext =', ciphertext)
    # print(type(ciphertext))
    room_name = codecs.encode(ciphertext, 'ascii', 'ignore').decode('unicode_escape')
    # print('room_name =',room_name)
    # print(type(room_name))
    group_name = room_name
    sanitized_group_name = re.sub(r'[^\w.-]', '', group_name)[:100]
    # print('sanitized_group_name =', sanitized_group_name)
    # print(type(sanitized_group_name))
    return sanitized_group_name


def room(request):
    if request.method == 'GET':
        request.session.save()
        session_key = request.session.session_key
        
        if not GroupChat.objects.filter(creator=request.session.session_key).exists():
            unique_code = aes_encryption(request.META['HTTP_HOST'], session_key)    
            print('unique_code_from_view', unique_code)
            GroupChat.objects.create(creator=session_key, 
                                     title='question_from = %s' % session_key,
                                     unique_code=unique_code)

    return render (request, 'chat/chatroom.html')