from django.conf.urls import url, include


from bot_register.views import TelegramView

urlpatterns = [
    url(r'^([-_:a-zA-Z0-9]+)/', TelegramView.as_view(), name='bot_hook')
]

# curl -d '{"key1":"value1", "key2":"value2"}' -H "Content-Type: application/json" -X POST http://localhost:8000/bot_register/736783073:AAHp2vnt5yZGU1kLh1iuB9y1ZgiuuW07_G4/