from django.contrib.sessions.backends.db import SessionStore as DbStore


class SessionStore(DbStore):
    @classmethod
    def get_model_class(cls):
        # Avoids a circular import and allows importing SessionStore when
        # django.contrib.sessions is not in INSTALLED_APPS.
        from ..models import CustomSession

        return CustomSession
    
    # def create_model_instance(self, data):
    #     """
    #     overriding the function to save the changes to db using `session["user_id"] = user.id` .
    #     This will create the model instance with the custom field values. 
    #     When you add more field to the custom session model you have to update the function 
    #     to handle those fields as well.
    #     """
    #     print('hi')
    #     obj = super().create_model_instance(data)

    #     print('bye')
    #     obj.created_at = data.get('created_at',)
    #     print(obj.created_at)
    #     obj.updated_at = data.get('updated_at')
    #     print('created_at')
    #     return obj
    