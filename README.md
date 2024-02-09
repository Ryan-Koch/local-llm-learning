# Happy fun learning time

This is a learning repo where I was playing around with the following things:
- Large Language Models (LLMs)
- Django
- HTMX
- Vector Datastores (Chroma) and searching them

To run this thing you need to do the following:
1. Install [Ollama](https://ollama.ai/). 
2. Setup a virtual environment: `python -m venv ./venv` (./venv can be the location of your choosing)
3. Activate your environment: `source activate <path to virtual environment>/bin/activate` (assuming you're on macos)
4. Install the dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Configure your local config files from the `.template` versions.
7. Setup gdocs authentication: [Lang chain docs](https://python.langchain.com/docs/integrations/document_loaders/google_drive)
8. Run the server `python manage.py runserver`

# What can this do?
- Currently it can take a folder ID from google drive and ingest all of the documents within it (not set to do recursive at the moment, but that's a flip of a flag to enable) and create a vector data store.
- It has a django app that will store questions asked to the LLM and is able to do a top k similarity search on the vector store to get answers.

# Some issues I'm thinking about
- The way you ask questions matters a lot and can impact the results found via the relevant document search. I'd like to find some user friendly ways to create some forgiveness here.
- Sometimes it gets tripped up when a document mentions multiple potential outcomes for a given question. A TDR for example talks about all the options considered, and while the model often gives the one chosen, I've seen it regularly go to the wrong one.
- I don't yet have it doing things in a conversational way where it carries context from interaction to interaction. I've set up the chat storage model to support separating groups of chats up so this is possible, but I haven't yet spent time on it.
- Right now this just does embedding using vector data, I'm not adding anything additional directly into the trained model. That might come later or in a different learning project.
- I'm currently moving the base URL config out of the DB and into a config file.
