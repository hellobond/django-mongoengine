import logging
from django.contrib import auth
from .models import User

logger = logging.getLogger(__name__)

class MongoEngineBackend(object):
    """Authenticate using MongoEngine and mongoengine.django.auth.User.
    """

    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False
    _user_doc = False

    # authenticate = auth.backends.ModelBackend.__dict__["authenticate"]
    # get_user = auth.backends.ModelBackend.__dict__["get_user"]

    def authenticate(self, username=None, password=None):
        user = self.user_document.objects(username=username).first()
        
        if user:
            if password and user.check_password(password):
                backend = auth.get_backends()[0]
                user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
                return user
        return None


    def get_user(self, user_id):
        # return self.user_document.objects.with_id(user_id)
        return User.objects.get(id=user_id)

    @property
    def user_document(self):
        if self._user_doc is False:
            from .models import get_user_document
            self._user_doc = get_user_document()
        return self._user_doc

def get_user(userid):
    """Returns a User object from an id (User.id). Django's equivalent takes
    request, but taking an id instead leaves it up to the developer to store
    the id in any way they want (session, signed cookie, etc.)
    """
    if not userid:
        return AnonymousUser()
    return MongoEngineBackend().get_user(userid) or AnonymousUser()
