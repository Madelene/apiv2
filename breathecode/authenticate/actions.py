import os
from django.contrib.auth.models import User, Group
from django.utils import timezone
from .models import Token
from breathecode.notify.actions import send_email_message

def get_user(github_id=None, email=None):
    user = None
    if email is not None:
        user = User.objects.get(email=email)
    return user

def create_user(github_id=None, email=None):
    user = None
    if email is not None:
        user = User.objects.get(email=email)
    return user

def delete_tokens(users=None, status='expired'):
    now = timezone.now()
    
    tokens = Token.objects.all()
    if users is not None:
        tokens = tokens.filter(user__id__in=[users])
    if status == 'expired':
        tokens = Token.objects.filter(expires_at__lt=now)

    count = len(tokens)
    tokens.delete()
    return count

def reset_password(users=None):
    for user in users:
        token = Token.create_temp(user)
        send_email_message('pick_password', user.email, {
            "LINK": os.getenv('API_URL') + f"/v1/auth/password/{token}"
        })
    
    return True