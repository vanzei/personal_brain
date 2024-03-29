import os
from typing import Any, Dict, List
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import ChatOpenAI
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
# Assuming BaseRetriever is the correct abstract base class to inherit from
from langchain.retrievers import BaseRetriever  # Ensure this import is correct based on LangChain's structureclass CustomRetriever(BaseRetriever):
def __init__(self, index, model, tokenizer):
    self.index = index
    self.model = model
    self.tokenizer = tokenizer

def _get_relevant_documents(self, query: str, top_k: int = 10):
    # Convert the query into embeddings using the model and tokenizer
    with torch.no_grad():
        inputs = self.tokenizer(query, return_tensors="pt", truncation=True, padding=True)
        outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)

    # Use the embeddings to query the Pinecone index
    search_results = self.index.query(vector=embeddings.tolist(), top_k=top_k)
    
    # Return the matches in the format expected by LangChain
    return search_results['matches']

# Usage in your run_llm function
def run_llm(query: str, chat_history: List[Dict[str, Any]] = []):
    custom_retriever = CustomRetriever(index, model, tokenizer)

    # Initialize other necessary components for ConversationalRetrievalChain
    # ...

    # Create the ConversationalRetrievalChain with the custom retriever
    conversational_chain = ConversationalRetrievalChain(
        retriever=custom_retriever,
        # other parameters like combine_docs_chain, question_generator, etc.
    )

    # Run the chain with the query and chat_history
    response = conversational_chain.run({
        "question": query,
        "chat_history": chat_history
    })
    return response