import os
from typing import Any, Dict, List
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv
import os

from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings

load_dotenv()
pinecone_key = os.getenv('PINECONE_API_KEY')
pinecone_env = os.getenv('PINECONE_ENVIRONMENT_REGION')
pinecone_index = os.getenv('INDEX_NAME')
openai_key = os.getenv('OPENAI_API_KEY')



openai_api_key = os.environ.get('OPENAI_API_KEY') or 'OPENAI_API_KEY'
model_name = 'text-embedding-ada-002'

embed = OpenAIEmbeddings(
    model=model_name,
    openai_api_key=openai_api_key
)

text_field = "text"


# Initialize Pinecone
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

from langchain.vectorstores import Pinecone
def run_query(query: str) -> List[Dict[str, Any]]:
    vectorstore = Pinecone(
        index, embed.embed_query, text_field
    )

    vectorstore.similarity_search(
        query,  # our search query
        k=3  # return 3 most relevant docs
    )

    from langchain.chat_models import ChatOpenAI
    from langchain.chains.conversation.memory import ConversationBufferWindowMemory
    from langchain.chains import RetrievalQA

    # chat completion llm
    llm = ChatOpenAI(
        openai_api_key=openai_api_key,
        model_name='gpt-3.5-turbo',
        temperature=0.0
    )
    # conversational memory
    conversational_memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        k=5,
        return_messages=True
    )
    # retrieval qa chain
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )

    from langchain.agents import Tool

    tools = [
        Tool(
            name='Knowledge Base',
            func=qa.run,
            description=(
                'use this tool when answering general knowledge queries to get '
                'more information about the topic'
            )
        )
    ]

    from langchain.agents import initialize_agent

    agent = initialize_agent(
        agent='chat-conversational-react-description',
        tools=tools,
        llm=llm,
        verbose=True,
        max_iterations=3,
        early_stopping_method='generate',
        memory=conversational_memory
    )

    return agent.run(query)
