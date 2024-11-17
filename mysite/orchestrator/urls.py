from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from orchestrator.views.knowledge_base import knowledge_view

urlpatterns = [
    path('api/add_to_knowledge/', csrf_exempt(knowledge_view), name='knowledge_view'),
]