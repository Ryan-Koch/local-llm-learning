import datetime
import uuid
import requests
import configparser

from django.http import HttpResponse
from django.shortcuts import render

from LLMLocalDjangoApp.models import ChatSession
from LLMLocalDjangoApp import vector_store


def display_base(request):
    return render(request, "LLMLocalDjangoApp/base.html")


def llm_interaction(request):
    # Get at the vector store and the base URL for the LLM API.
    vs_c = vector_store.VectorStore()
    url_setting = vs_c.get_base_url()
    url_for_request = url_setting + "/api/generate"

    global_config = configparser.ConfigParser()
    global_config.read("global_settings.local")

    # This is the chat input from the user.
    chat_input = request.POST["message"]
    # Save a timestamps for the chat input (gets saved in the chat model)
    timestamp_chat = datetime.datetime.utcnow()

    # get access to the chroma store
    store = vs_c.initialize_store()
    # using MMR search for now:
    # https://python.langchain.com/docs/modules/data_connection/retrievers/vectorstore#maximum-marginal-relevance-retrieval
    retriever = store.as_retriever(search_type="mmr")

    relevant_docs = retriever.get_relevant_documents(query=chat_input)

    docs_for_prompt = []
    for doc in relevant_docs:
        docs_for_prompt.append(f"Title: {doc.metadata['title']}\n\n{doc.page_content}\n\nSource: {doc.metadata['source']}\n\n")

    text_for_prompt = "\n\n".join(docs_for_prompt)
    print(text_for_prompt)

    # template prompt, we inject both what was found in the relevant docs search and the chat input (as the question
    # to be answered).
    prompt = f"""You answer questions about the contents of decision record documents used by the Truss organization. 
    Please provide links and titles for the source documentation you reference to come up with your response. 
    As you answer don't make information up, if you can't find it or don't know, answer that you don't know. 
    What is the answer to the following question: {chat_input}? Please make use of the following context to 
    inform how you respond. \n{text_for_prompt}\n\n"""

    # This dumps out the whole LLM response in one go instead of doing the streaming text thing that folks might be
    # used to seeing from ChatGPT. Maybe later I'll try and do that too, since HTMX can support the interaction.
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

    # This sends an HX-Trigger header, which signals the front end to send an request to the server to get the chats
    # that have been saved to the DB so far.
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
