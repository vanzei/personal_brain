from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from typing import List, Optional, Union, List
from dotenv import load_dotenv
import os
import psycopg2
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from schema import Book, Paper, Document

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DBNAME = os.getenv('POSTGRES_DBNAME')

MONGO_INITDB_ROOT_USERNAME = os.getenv('MONGO_INITDB_ROOT_USERNAME')
MONGO_INITDB_ROOT_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
local_IP = os.getenv('local_IP')

app = FastAPI()

# MongoDB connection URI
client = MongoClient(f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@{local_IP}", 27017)

# Select your database
db = client['data']

# Select your collection
book_collection = db['Books']
paper_collection = db['Papers']


try:
    connPostgres = psycopg2.connect(database = f"{POSTGRES_DBNAME}", 
                            user = f"{POSTGRES_USER}", 
                            host= f'{local_IP}',
                            password = f"{POSTGRES_PASSWORD}",
                            port = 5432)
except:
    print("I am unable to connect to the database") 
cursor = connPostgres.cursor()


    
# @app.post("/books/", response_description="Add new book", response_model=Book)
# async def create_book(book: Book):
#     book = dict(book)  # Convert Pydantic model to dict
#     result = collection.insert_one(book)
#     new_book = collection.find_one({"_id": result.inserted_id})
#     if new_book:
#         return Book(**new_book)
#     else:
#         raise HTTPException(status_code=500, detail="Failed to create book.")
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url='/docs')

@app.get("/books/", response_description="List all books", response_model=List[Book], tags=["API Check Books"])
async def list_books():
    books = list(book_collection.find())
    return [Book(**book) for book in books]

    
@app.get("/books/{ISBN10}", response_description="Get a single book by ISBN10", response_model=Book, tags=["API Check Books"])
async def get_book(ISBN10: str):
    book = book_collection.find_one({"ISBN10": ISBN10})
    if book:
        return Book(**book)
    else:
        raise HTTPException(status_code=404, detail=f"Book with ID {ISBN10} not found")


@app.get("/field/", response_description="Get books by field", response_model=List[Book], tags=["API Check Books per Field"])
async def get_books_by_field(field: str):
    books = list(book_collection.find({"field": field}))

    if books:
        return [Book(**book) for book in books]
    else:
        raise HTTPException(status_code=404, detail=f"No books found for field {field}")

@app.get("/papers/", response_description="List all papers", response_model=List[Paper], tags=["API Check Papers"])
async def list_papers():
    papers = list(paper_collection.find())
    return [Paper(**paper) for paper in papers]


@app.get("/all/", response_description="List all papers and books", response_model=List[Document], tags=["API Check All Documents"])
async def list_papers():
    papers = list(paper_collection.find())
    books = list(book_collection.find())

    documents = []
     
    for paper in papers:
        document = {}
        document['name'] = paper['paper_name']
        document['content'] = paper['content']
        document['field'] = paper['field']
        documents.append(document)
    
    for book in books:
        document = {}
        document['name'] = book['book_name']
        document['content'] = book['content']
        document['field'] = book['field']
        documents.append(document)

    doc_return = [Document(**doc) for doc in documents]
    return doc_return
