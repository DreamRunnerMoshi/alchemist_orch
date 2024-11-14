import json
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


import logging

from orchestrator.embedding.chroma_embedding import DocumentToIndex, index_doc
logger = logging.getLogger('alchemist_urls')

@csrf_exempt
@require_POST
def knowledge_view(request):
    try:
        logger.error("Request body: %s", request.body)
        body = json.loads(request.body)
        doc_to_index = DocumentToIndex(title=body.get('text'), text=body.get('pageTitle'), url=body.get('pageUrl'))
        index_doc(doc_to_index)
    except json.JSONDecodeError:
        logger.error("Invalid JSON received")
        return HttpResponse("Invalid JSON", status=500)
    
    return HttpResponse("data added to index", status=200)
