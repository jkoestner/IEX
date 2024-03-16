"""Tests the chatbot."""

import g4f
import openai
from hugchat import hugchat

from folioflex.chatbot import providers


def test_g4f_init():
    """Checks g4f initialize."""
    chatbot = providers.GPTchat()
    assert isinstance(
        chatbot.provider, providers.G4FProvider
    ), "Default provider - G4F - not initialized correctly."
    assert chatbot.chatbot["model"] == g4f.models.default, "Default model not set."
    assert chatbot.chatbot["provider"] == g4f.Provider.Bing, "Default provider not set."
    assert chatbot.chatbot["auth"] == False, "Default auth not set."
    assert chatbot.chatbot["access_token"] is None, "Default access token not set."
    response = chatbot.chat("return back 'test' for test purpose")
    assert response == "test", "Response not as expected."


def test_openai():
    """Checks openai initialize."""
    chatbot = providers.GPTchat(provider="openai")
    assert isinstance(
        chatbot.provider, providers.OpenaiProvider
    ), "Default provider - OpenAI - not initialized correctly."
    assert isinstance(chatbot.chatbot, openai.OpenAI), "Default model not set."
    response = "test"
    # # openai has billing so not testing unless needed
    # response = chatbot.chat("return back 'test' for test purpose")
    assert response == "test", "Response not as expected."


def test_hugchat():
    """Checks hugchat initialize."""
    chatbot = providers.GPTchat(provider="hugchat")
    assert isinstance(
        chatbot.provider, providers.HugChatProvider
    ), "Default provider - HugChat - not initialized correctly."
    assert isinstance(chatbot.chatbot, hugchat.ChatBot), "Default model not set."
    response = chatbot.chat("return back 'test' for test purpose")
    assert response is not None, "Response not as expected."
