import os
from typing import Any, Dict, List
from pinecone import Pinecone, ServerlessSpec
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv
import os
from transformers import AutoModel, AutoTokenizer
import torch

load_dotenv()
pinecone_key = os.getenv('PINECONE_API_KEY')
pinecone_env = os.getenv('PINECONE_ENVIRONMENT_REGION')
pinecone_index = os.getenv('INDEX_NAME')
# Initialize Pinecone
pc = Pinecone(api_key=pinecone_key)

index_name = pinecone_index  # Replace with your actual index name
dimension = 384  # Dimension of your embeddings
metric = "cosine"  # Metric for the vector space

# Retrieve the list of indexes and check if your index exists
indexes_info = pc.list_indexes()
index_names = [index["name"] for index in indexes_info]  # Assuming list_indexes() returns a list of dictionaries

# Check if the index exists, and create it if not
if index_name not in index_names:
    pc.create_index(
        name=index_name, 
        dimension=dimension, 
        metric=metric,
        spec=ServerlessSpec(
            cloud='gcp',  # Or 'gcp', based on your preference
            region=pinecone_env  # Choose the region closest to you or your users
        )
    )


# Access the Pinecone index
index = pc.Index(name=index_name)

# Load a Hugging Face model and tokenizer
model_name = 'sentence-transformers/all-MiniLM-L6-v2'  # Example model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def get_embeddings(text: str):
    with torch.no_grad():
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings.numpy()

def run_llm(query: str, chat_history: List[Dict[str, Any]] = []):
    embeddings = get_embeddings(query)
    
    # Query the Pinecone index
    top_k_results = 10
    search_results = index.query(vector=embeddings.tolist(), top_k=top_k_results)

    # Process the search_results to match the expected dictionary format for the retriever
    retriever_results = {
        'data': search_results.get('matches', [])
    }

    chat = ChatOpenAI(
        verbose=True,
        temperature=0
    )

    # Ensure the retriever argument receives the correctly formatted dictionary
    qa = ConversationalRetrievalChain.from_llm(
        llm=chat, 
        retriever=retriever_results, 
        return_source_documents=True
    )
    return qa({"question": query, "chat_history": chat_history})
