import datetime
import uuid

import requests
from django.http import HttpResponse
from django.shortcuts import render

from LLMLocalDjangoApp.models import Setting

from LLMLocalDjangoApp.models import ChatSession

from LLMLocalDjangoApp import vector_store


def display_base(request):
    return render(request, "LLMLocalDjangoApp/base.html")


def llm_interaction(request):
    url_setting = Setting.objects.all().filter(setting_name="llm_url")[0].setting_value
    chat_input = request.POST["message"]

    url_for_request = url_setting + "api/generate"

    timestamp_chat = datetime.datetime.utcnow()

    vs_c = vector_store.VectorStore()
    store = vs_c.initialize_store()
    relevant_docs = store.similarity_search(chat_input, k=10)

    # template prompt, we inject both what was found in the relevant docs search and the chat input (as the question to be answered).
    prompt = f"You answer questions about the contents of decision record documents used by the Truss organization. As you answer these questions don't make information up, if you can't find it or don't know, it's okay to say so. Given the following documentation: {relevant_docs}\n What is the best answer to this question: {chat_input}?"

    # This dumps out the whole LLM response in one go instead of doing the streaming text thing that folks might be used to seeing from ChatGPT. Maybe later I'll try and do that too, since HTMX can support the interaction.
    response = requests.post(
        url_for_request, json={"prompt": prompt, "model": "llama2", "stream": False}
    )

    if response.status_code == 200:
        response_timestamp = datetime.datetime.utcnow()
        chat_sessions = ChatSession.objects.all()
        if len(chat_sessions) == 0:
            chat_session = ChatSession(session_name="default", session_id=uuid.uuid4())
            chat_session.save()
            chat_sessions.append(chat_session)
        chat_session = chat_sessions[0]
        chat_session.chats.create(
            chat_text=chat_input,
            response_text=response.json()["response"],
            chat_id=uuid.uuid4(),
            timestamp_chat=timestamp_chat,
            timestamp_response=response_timestamp,
        )
    # Okay, so a hacky thing I did is have this POST save stuff to the DB and then use the HX-Trigger event to trigger a GET to the chats_for_session view below.
    return HttpResponse(
        response.json()["response"], headers={"HX-Trigger": "send-event"}
    )


# This is what populates the page via a GET with chats that have been saved to the DB so far.
def chats_for_session(request):
    chat_sessions = ChatSession.objects.all()
    if len(chat_sessions) == 0:
        chat_session = ChatSession(session_name="default", session_id=uuid.uuid4())
        chat_session.save()
        chat_sessions.append(chat_session)
    chat_session = chat_sessions[0]
    chats = chat_session.chats.order_by("timestamp_chat")
    html_chats = ""
    for chat in chats:
        html_chats = (
            html_chats
            + "<div class='chat-message'><div class='chat-message-inner'><p>"
            + chat.chat_text
            + "</p></div></div>"
        )
        html_chats = (
            html_chats
            + "<div class='response-message'><div class='response-message-inner'><p>"
            + chat.response_text
            + "</p></div></div>"
        )
    return HttpResponse(html_chats)
