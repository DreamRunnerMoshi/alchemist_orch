import json
from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

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

@csrf_exempt
@require_GET
def embedding_view(request):
    if request.method == 'GET':
        return render(request, 'knowledge_base.html')
    else:
        return HttpResponse("Method not allowed", status=405)

@csrf_exempt
@require_GET
def query_embedding(request):
    query = request.GET.get('query', '')
    if not query:
        return HttpResponse("Query parameter is required", status=400)
    
    chroma_embedding = ChromaEmbedding()
    results = chroma_embedding.search_chroma(query=query, n_results=3)
    
    # Convert SearchResult objects to dictionaries
    results_dict = [result.to_dict() for result in results]
    
    return HttpResponse(json.dumps(results_dict), content_type="application/json")


