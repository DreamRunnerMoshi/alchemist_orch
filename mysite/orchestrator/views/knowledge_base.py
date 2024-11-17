import json
import pprint
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


import logging

from orchestrator.embedding.chroma_embedding import DocumentToIndex, ChromaEmbedding
logger = logging.getLogger('alchemist_urls')

@csrf_exempt
@require_POST
def knowledge_view(request):
    try:
        body = json.loads(request.body)

        title = body.get('pageTitle')
        text = body.get('text')
        url = body.get('pageUrl')

        doc_to_index = DocumentToIndex(title=title, text=text, url=url)
        ChromaEmbedding().index_doc(doc_to_index)
    except json.JSONDecodeError:
        logger.error("Invalid JSON received")
        return HttpResponse("Invalid JSON", status=500)
    
    return HttpResponse("data added to index", status=200)
