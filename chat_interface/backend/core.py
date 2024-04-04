import os
from openai import OpenAI
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory

load_dotenv()

# Load API keys and other environment variables
pinecone_key = os.getenv('PINECONE_API_KEY')
pinecone_index = os.getenv('PINECONE_INDEX_NAME')
openai_key = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI client
client = OpenAI(api_key=openai_key)

# Initialize embeddings
embeddings = OpenAIEmbeddings()


# Initialize Pinecone client with the configuration object
index_name = 'prof-library'   # Replace with your actual index name
dimension = 1536  # Dimension of your embeddings
metric = "cosine"  # Metric for the vector space
vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)

def run_query(query, memory):# Initialize the language model
    llm = ChatOpenAI(
        openai_api_key=openai_key,
        model_name='gpt-3.5-turbo',
        temperature=0.0
    )

    # Initialize RetrievalQA with memory and retriever
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        memory=memory)

    # Perform question answering
    
    res = qa.invoke(query)
    print(res)
    return res['result'], memory 