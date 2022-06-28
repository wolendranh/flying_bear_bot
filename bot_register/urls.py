from django.urls import include, re_path


from bot_register.views import TelegramView

urlpatterns = [
    re_path(r'^([-_:a-zA-Z0-9]+)/', TelegramView.as_view(), name='bot_hook')
]
