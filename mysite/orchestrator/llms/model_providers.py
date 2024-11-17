import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

"""
This class will provide GPT model based on .env file.
It has a method get_model, which will return OpenGPT model or Ollama model based on the model name provided in .env file.
"""

class ModelParams:
    GPT_SOURCE = 'GPT_SOURCE'
    MODEL_NAME = 'MODEL_NAME'
    TEMPERATURE = 'TEMPERATURE'

class ModelSources:
    OPENAI = 'OpenAI'
    OLLAMA = 'Ollama'

class ModelProvider:
    def __init__(self):
        load_dotenv()
        self.gpt_source = os.getenv(ModelParams.GPT_SOURCE)
        self.model_name = os.getenv(ModelParams.MODEL_NAME)
        self.temperature = float(os.getenv(ModelParams.TEMPERATURE, 0.5))

    def get_model(self):
        if self.gpt_source == ModelSources.OPENAI:
            return self._get_open_gpt_model()
        elif self.gpt_source == ModelSources.OLLAMA:
            return self._get_ollama_model()
        else:
            return self._get_ollama_model()

    def _get_open_gpt_model(self):
        return ChatOpenAI(
            model=self.model_name, 
            temperature=self.temperature, 
            streaming=True
        )

    def _get_ollama_model(self):
        return ChatOllama(
            model="llama3.2:3b",
            temperature=self.temperature,
            # other params...
        )

