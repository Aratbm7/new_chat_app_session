from django.contrib.sessions.backends.db import SessionStore as DBStore
import chat
from django.utils import timezone

class SessionStore(DBStore):

    @classmethod
    def get_model_class(cls):
        print('helllo')
        return chat.models.CustomSession

    def create_model_instance(self, data):
        """
        overriding the function to save the changes to db using `session["user_id"] = user.id` .
        This will create the model instance with the custom field values. 
        When you add more field to the custom session model you have to update the function 
        to handle those fields as well.
        """
        print('hi')
        # data.pop('updated_at')
        obj = super().create_model_instance(data)
    
        create = data.pop('created_at')
        print('create_pop ' + create)

        print('bye')
        # obj.created_at = data.pop('created_at',)
        # print(obj.created_at)
        # obj.updated_at = data.pop('updated_at')
        print('created_at')
        return obj