from django.conf.urls import url, include


from bot_register.views import TelegramView

urlpatterns = [
    url(r'^([-_:a-zA-Z0-9]+)/', TelegramView.as_view(), name='bot_hook')
]
