import os
import json
import requests
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from tqdm import tqdm
import torch
from transformers import AutoTokenizer, AutoModel
# Load environment variables
load_dotenv()
pinecone_key = os.getenv('PINECONE_API_KEY')
pinecone_env = os.getenv('PINECONE_ENVIRONMENT_REGION')
pinecone_index = os.getenv('INDEX_NAME')
local_IP = os.getenv('local_IP')

model_name = "sentence-transformers/all-MiniLM-L12-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Function to generate embeddings
def generate_embeddings(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).numpy()
    return embeddings

pc = Pinecone(api_key=pinecone_key)

index_name = pinecone_index  # Replace with your actual index name
dimension = 1536  # Dimension of your embeddings
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

response = requests.get(f"http://{local_IP}/all")
resp_json = json.loads(response.text)

names_available = [item['name'] for item in resp_json]
print(names_available)
def ingest_docs(resp_json):
    # Fetch documents from your local service


    for item in tqdm(resp_json):
        # if item['name'] in names_available:
        #     index.delete(ids=[item['name']])
        #     print(str(item['name']) + ' was deleted to Pinecone')

        embedding = generate_embeddings(item["content"])
        # Flatten the embedding to a 1D list of floats
        embedding_flat = embedding.flatten().tolist()
        index.upsert(vectors=[(item["name"], embedding_flat)])
        print(str(item['name']) + ' was Loaded to Pinecone')

if __name__ == "__main__":
    ingest_docs(resp_json)
