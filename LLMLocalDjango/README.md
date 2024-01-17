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
6. Put some PDF documents in `static/documents` (the start up process specifically looks for PDFs and will ignore other things).
7. Run the server `python manage.py runserver`

There is a `default_data.json` that seeks to add the initial `Settings` objects in the DB for you. It uses default values based on what I had going on using Ollama locally. You can change these values though in the Django Admin app at any time.

# Some issues I'm thinking about
- The way you ask questions matters a lot and can impact the results found via the relevant document search. I'd like to find some user friendly ways to create some forgiveness here.
- Sometimes it gets tripped up when a document mentions multiple potential outcomes for a given question. A TDR for example talks about all the options considered, and while the model often gives the one chosen, I've seen it regularly go to the wrong one.
- I don't yet have it doing things in a conversational way where it carries context from interaction to interaction. I've set up the chat storage model to support separating groups of chats up so this is possible, but I haven't yet spent time on it.
- Right now this just does embedding using vector data, I'm not adding anything additional directly into the trained model. That might come later or in a different learning project.

