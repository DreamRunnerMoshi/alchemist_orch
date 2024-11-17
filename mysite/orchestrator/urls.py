from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from orchestrator.views.knowledge_base import knowledge_view, embedding_view, query_embedding

urlpatterns = [
    path('api/add_to_knowledge/', csrf_exempt(knowledge_view), name='knowledge_view'),
    path('embedding_view/', csrf_exempt(embedding_view), name='embedding_view'),
    path('api/query_embedding/', csrf_exempt(query_embedding), name='query_embedding'),
]