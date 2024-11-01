from django.urls import path
from .views import Dialogflow_webhook

urlpatterns=[
    path('dialogflow-webhook/',Dialogflow_webhook,name='dialogflow_webhook'),
]