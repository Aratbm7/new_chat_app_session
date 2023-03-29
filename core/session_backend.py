from django.contrib.sessions.backends.db import SessionStore as DBStore
from django.utils.functional import cached_property
from django.conf import settings
from account.middleware import get_current_request


class SessionStore(DBStore):

    @classmethod
    def get_model_class(cls):
        from account.models import CustomSession
        return CustomSession

    
            
    
    def create_model_instance(self, data):
        
        request = get_current_request()  
        print('request: %s' % request)     
        # print('ip: %s' % ip)
        # print('request.user.username: %s' % request.user.username)
        print('hello')
        
        custom_session_instance = self._get_session_from_db()
        print(custom_session_instance)
        
        email = None
        name = None
        if not custom_session_instance:
            date_created = None
            ip = request.META.get('REMOTE_ADDR') 
            print('new_ip: %s' % ip)
            
            
        else:
            date_created = custom_session_instance.created_at
            ip = request.META.get('REMOTE_ADDR') 
            stored_ip = custom_session_instance.ip
            if request.user.is_authenticated:
                name = request.user.username
                email = request.user.email
            if stored_ip == ip:
                print('stored_ip')
                ip = ip
            else: print('ip is changed')

        return self.model(
            session_key=self._get_or_create_session_key(),
            session_data=self.encode(data),
            expire_date=self.get_expiry_date(),
            created_at = date_created,
            ip = ip,
            name =name,
            email = email,

       )