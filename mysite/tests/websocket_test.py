from channels.testing import WebsocketCommunicator
from django.test import TestCase
from mysite.asgi import application

class ChatWithDocumentViewTestTestCase(TestCase):
    async def test_websocket_connection(self):
        communicator = WebsocketCommunicator(application, "/ws/chatgpt/")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        # Test sending and receiving messages
        await communicator.send_json_to({"text": "Hello"})
        response = await communicator.receive_json_from()
        self.assertEqual(response, {"expected_response": "value"})

        await communicator.disconnect()