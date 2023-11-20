# JWT �������� - ���ؼ�

## 1. ����ȯ�� ����
### 1-1. ������Ʈ ���丮 ���� �� �̵�
```bash
mkdir jwt-practice
cd jwt-practice
```
### 1-2. ����ȯ�� ����
```bash
python -m venv venv
```
### 1-3. ����ȯ�� Ȱ��ȭ
```bash
source ./venv/bin/activate
```
### 1-4. �ʿ� ��� ��ġ
```
# requirements.txt
asgiref==3.7.2
certifi==2023.7.22
cffi==1.16.0
charset-normalizer==3.3.2
cryptography==41.0.5
defusedxml==0.7.1
dj-rest-auth==2.2.4
Django==4.0.3
django-allauth==0.50.0
djangorestframework==3.13.1
djangorestframework-simplejwt==5.1.0
idna==3.4
oauthlib==3.2.2
pycparser==2.21
PyJWT==2.8.0
python3-openid==3.2.0
pytz==2023.3.post1
requests==2.31.0
requests-oauthlib==1.3.1
sqlparse==0.4.4
typing_extensions==4.8.0
tzdata==2023.3
urllib3==2.0.7
```

```bash
pip install -r requirements.txt
```

## 2. ��� ������Ʈ �⺻ ����
### 2-1. ��� ������Ʈ ����
```bash
django-admin startproject project .
```
### 2-2. accounts �� ����
```bash
python manage.py startapp accounts
```
### 2-3. project/settings.py ����
```python
from datetime import timedelta
...
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    ...
    "accounts",
    # ��ġ�� ���̺귯����
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
]
...

# dj-rest-auth
REST_USE_JWT = True # JWT ��� ����
JWT_AUTH_COOKIE = 'my-app-auth' # ȣ���� Cookie Key ��
JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token' # Refresh Token Cookie Key ��

# django-allauth
SITE_ID = 1 # �ش� ������ id
ACCOUNT_UNIQUE_EMAIL = True # User email unique ��� ����
ACCOUNT_USER_MODEL_USERNAME_FIELD = None # ����� �̸� �ʵ� ����
ACCOUNT_USERNAME_REQUIRED = False # User username �ʼ� ����
ACCOUNT_EMAIL_REQUIRED = True # User email �ʼ� ����
ACCOUNT_AUTHENTICATION_METHOD = 'email' # �α��� ���� ����
ACCOUNT_EMAIL_VERIFICATION = 'none' # email ���� �ʼ� ����

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # AccessToken ��ȿ �Ⱓ ����
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),  # RefreshToken ��ȿ �Ⱓ ����
}
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
```

## 3. Model �ۼ�
### 3-1. accounts/managers.py
```python
# accounts/managers.py
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
```
### 3-2. accounts/models.py
```python
# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

GENDER_CHOICES = (
    ('male', '����'),
    ('female', '����'),
)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    

    def __str__(self):
        return self.email
```

### 3-3. project/settings.py�� �߰�
```python
AUTH_USER_MODEL = 'accounts.CustomUser'
```

### 3-4. accounts/admin.py
```python
from django.contrib import admin
from accounts.models import CustomUser

admin.site.register(CustomUser)
```

### 3-5. �� ������� ����
```bash
python manage.py makemigrations
python manage.py migrate
```

## 4. URL ����
### 4-1. project/urls.py
```python
# project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("account/", include("accounts.urls"))
]
```

### 4-2. accounts/urls.py
```python
# accounts/urls.py
from django.urls import path, include
from .views import mypage

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path('join/', include("dj_rest_auth.registration.urls")),
    path('mypage/', mypage),
]
```

## 5. Views ����
### 5-1. accounts/views.py
```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mypage(request):
    content = {'message': f'�ݰ����ϴ�, {str(request.user)}��!'}
    return Response(content)
```

## 6. ���� �׽�Ʈ
### 6-1. ���� ����
```bash
python manage.py runserver
```

### 6-2. ȸ������ �׽�Ʈ
**Request**
- URL: http://127.0.0.1:8000/account/join/
- Method: POST
- Body
```json
{
    "email": "test@test.com",
    "password1": "testest1234",
    "password2": "testest1234"
}
```

**Response**
```json
Status: 201 Created
Size: 567 Bytes
Time: 408 ms
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwMjExNTgzLCJpYXQiOjE3MDAyMDc5ODMsImp0aSI6IjgyMzdjOTc2ZmM2MDQyNmU5NGIwNTNjYjRmOTczYWVlIiwidXNlcl9pZCI6M30.L2H06mtR-5I29VenREJEg8N58Cl_oVKciddEyP9P3V0",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwMDI5NDM4MywiaWF0IjoxNzAwMjA3OTgzLCJqdGkiOiJmMzUxYjdjYTYyYmE0NjE4YmU3MzA1YWVmOTliM2I0MSIsInVzZXJfaWQiOjN9.Ie083rWoKK0rLoM1ciI-sZ3ZjU9kfyygBFc_ZE-B0Ag",
  "user": {
    "pk": 3,
    "email": "test@test.com",
    "first_name": "",
    "last_name": ""
  }
}
```

### 6-3. �α��� �׽�Ʈ
#### 6-3-1. ��ȿ�� ��ū�� ������ ���
**Request**
- URL: http://127.0.0.1:8000/account/login/
- Method: POST
- Header
```json
{
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwMjExNzA3LCJpYXQiOjE3MDAyMDgxMDcsImp0aSI6IjA2OGUzMDgzNTdmNzQzNTQ5Yjc5ODAxMjRmOThlN2Y4IiwidXNlcl9pZCI6M30.BEDBXTcawX7FbbDitgPhSUxDyWED6qnFNKPgpyEg6Y8"
}
```
- Body
```json
{
    "email": "test@test.com",
    "password": "testest1234"
}
```

**Response**
```json
Status: 200 OK
Size: 566 Bytes
Time: 666 ms
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwMjExNzA3LCJpYXQiOjE3MDAyMDgxMDcsImp0aSI6IjA2OGUzMDgzNTdmNzQzNTQ5Yjc5ODAxMjRmOThlN2Y4IiwidXNlcl9pZCI6M30.BEDBXTcawX7FbbDitgPhSUxDyWED6qnFNKPgpyEg6Y8",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwMDI5NDUwNywiaWF0IjoxNzAwMjA4MTA3LCJqdGkiOiI5OWNlZWIwZTFjMjY0ZjUzYTA1MDgyOWJiYTA1YmRhOSIsInVzZXJfaWQiOjN9.oRjClVqknwfzdMolSShiclgOrKClu_W6NUb0ZBENNkE",
  "user": {
    "pk": 3,
    "email": "test@test.com",
    "first_name": "",
    "last_name": ""
  }
}
```

#### 6-3-2. ��ȿ���� ���� ��ū�� ������ ���
**Request**
- URL: http://127.0.0.1:8000/account/login/
- Method: POST
- Header
```json
{
    "Authorization": "Bearer eyJhbGciOnJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwMjExNzA3LCJpYXQiOjE3MDAyMDgxMDcsImp0aSI6IjA2OGUzMDgzNTdmNzQzNTQ5Yjc5ODAxMjRmOThlN2Y4IiwidXNlcl9pZCI6M30.BEDBXTcawX7FbbDitgPhSUxDyWED6qnFNKPgpyEg6Y8"
}
```
- Body
```json
{
    "email": "test@test.com",
    "password": "testest1234"
}
```

**Response**
```json
Status: 401 Unauthorized
Size: 183 Bytes
Time: 23 ms
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

### 6-4. �α׾ƿ� �׽�Ʈ
**Request**
- URL: http://127.0.0.1:8000/account/logout/
- Method: POST

**Response**
```json
Status: 200 OK
Size: 41 Bytes
Time: 46 ms
{
  "detail": "�α׾ƿ��Ǿ����ϴ�."
}
```

### 6-5. ���������� ���� �׽�Ʈ
#### 6-5-1. ��ȿ�� ��ū�� ������ ���
**Request**
- URL: http://127.0.0.1:8000/account/mypage/
- Method: GET
- Header
```json
{
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwMjExNzA3LCJpYXQiOjE3MDAyMDgxMDcsImp0aSI6IjA2OGUzMDgzNTdmNzQzNTQ5Yjc5ODAxMjRmOThlN2Y4IiwidXNlcl9pZCI6M30.BEDBXTcawX7FbbDitgPhSUxDyWED6qnFNKPgpyEg6Y8"
}
```
- Body
```json
{
    "email": "test@test.com",
    "password": "testest1234"
}
```

**Response**
```json
Status: 200 OK
Size: 48 Bytes
Time: 69 ms
{
  "message": "�ݰ����ϴ�, test@test.com��!"
}
```

#### 6-5-2. ��ȿ���� ���� ��ū�� ������ ���
**Request**
- URL: http://127.0.0.1:8000/account/mypage/
- Method: GET
- Header
```json
{
    "Authorization": "Bearer eyJhbGciOnJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwMjExNzA3LCJpYXQiOjE3MDAyMDgxMDcsImp0aSI6IjA2OGUzMDgzNTdmNzQzNTQ5Yjc5ODAxMjRmOThlN2Y4IiwidXNlcl9pZCI6M30.BEDBXTcawX7FbbDitgPhSUxDyWED6qnFNKPgpyEg6Y8"
}
```
- Body
```json
{
    "email": "test@test.com",
    "password": "testest1234"
}
```

**Response**
```json
Status: 401 Unauthorized
Size: 183 Bytes
Time: 23 ms
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```