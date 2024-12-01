# views.py
import asyncio
import json
import time
import uuid
from venv import logger
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from orchestrator.data_models.data_models import json_to_model
from orchestrator.llms.AlchemistGPT import AlchemistGPT  # Import AlchemistGPT

#alchemist = AlchemistGPT()  # Initialize AlchemistGPT
from typing import List, Optional
import uuid
import time

def _generate_gpt_strucuture(answer: str, data_index: int):
    return {
            "id": str(uuid.uuid4()),
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": "alchemist-beta",
            "choices": [
                {
                    "index": data_index,
                    "delta": {
                        "content": answer,
                        "role": "assistant"
                    }
                }
            ]
        }

@csrf_exempt
def alchemist_chat_view(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            # Process the request body as needed
            # For example, you can call an external API or handle the chat logic here
            alchemist_gpt = AlchemistGPT()
            async def event_stream():
                logger.error("Starting event stream")
                stream = await alchemist_gpt.astream(body)
                data_index = 0
                if stream is not None:
                    async for chunk in stream:
                        answer = chunk.get('answer')
                        if answer is not None:
                            response = _generate_gpt_strucuture(answer, data_index)
                            yield f"data: {json.dumps(response)}\n\n"
                        else:
                            response = _generate_gpt_strucuture(None, data_index)
                        
                        data_index = data_index + 1
            return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)