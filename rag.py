from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

client = OpenAI(api_key=api_key)

# Define file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_FILES = [
    os.path.join(BASE_DIR, 'decision-aid-content.txt'),
    os.path.join(BASE_DIR, 'examples_sensitive_response.txt'),
    os.path.join(BASE_DIR, 'example_mental_health.txt')
]

# Load and split documents
def create_vectorstore():
    documents = []
    for path in RESOURCE_FILES:
        loader = TextLoader(path)
        documents.extend(loader.load())
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(documents)
    embedding = OpenAIEmbeddings()
    db = FAISS.from_documents(chunks, embedding)
    db.save_local("faiss_rag_index")

# Retrieve top-k relevant context
def retrieve_context(query, k=4):
    embedding = OpenAIEmbeddings()
    db = FAISS.load_local("faiss_rag_index", embedding)
    results = db.similarity_search(query, k=k)
    return "\n\n".join([doc.page_content for doc in results])

# Load conversation history
HISTORY_FILE = "history.json"
HISTORY_LENGTH = 4

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_history(user, bot):
    history = load_history()
    history.append({"user": user, "bot": bot})
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)

# Main function to generate response
def get_gpt_response(user_input):
    context = retrieve_context(user_input)
    cur_history = load_history()[-HISTORY_LENGTH:]
    formatted_history = "\n".join([
        f"User: {entry['user']}\nPrEPBot: {entry['bot']}" for entry in cur_history
    ]) if cur_history else ""

    system_prompt = (
        f"You are ShesPrEPared, a friendly assistant for HIV prevention and PrEP counseling.\n"
        f"Use clear, simple language. Avoid jargon.\n\n"
        f"Conversation History:\n{formatted_history}\n\n"
        f"Relevant Information:\n{context}\n\n"
        f"Now respond to the user question below in clear, friendly language."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=400,
            temperature=0.7
        )
        gpt_response = response.choices[0].message.content
        save_history(user_input, gpt_response)
        return gpt_response
    except Exception as e:
        return f"GPT experienced an internal error: {str(e)}"

if __name__ == '__main__':
    # Uncomment below if you want to build the index initially
    # create_vectorstore()
    user_input = input("Ask ShesPrEPared a question: ")
    print(get_gpt_response(user_input))
