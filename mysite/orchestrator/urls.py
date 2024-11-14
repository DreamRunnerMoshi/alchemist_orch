from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from orchestrator.views.chat_with_document_async import generate_response
from orchestrator.views.embedding_doc import knowledge_view
from orchestrator.views.views import send_message, index
from orchestrator.views.chat_with_document import ChatWithDocumentView

urlpatterns = [
    path("", index, name="index"),
    path('api/send-message/', generate_response, name='send_message'),
    path('api/chat_with_document/', csrf_exempt(ChatWithDocumentView.as_view()), name='chat_with_document'),
    path('api/add_to_knowledge/', csrf_exempt(knowledge_view), name='knowledge_view'),
]