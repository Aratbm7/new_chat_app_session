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
        Return a new instance of the session model object, which represents the
        current session state. Intended to be used for saving the session data
        to the database.
        """
        custom_session_instance = self._get_session_from_db()
        if not custom_session_instance:
            date_created = None
        else:
            date_created = custom_session_instance.created_at
        return self.model(
            session_key=self._get_or_create_session_key(),
            session_data=self.encode(data),
            expire_date=self.get_expiry_date(),
            created_at = date_created
        )