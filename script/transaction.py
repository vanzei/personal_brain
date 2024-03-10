# %%
from pymongo import MongoClient
from sqlalchemy import create_engine, Table, MetaData, insert
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DBNAME = os.getenv('POSTGRES_DBNAME')



MONGO_INITDB_ROOT_USERNAME= os.getenv('MONGO_INITDB_ROOT_USERNAME')
MONGO_INITDB_ROOT_PASSWORD= os.getenv('MONGO_INITDB_ROOT_PASSWORD')

# %%
def create_user(name, username, password, email, user_field, years, country):
    engine = create_engine(f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost/{POSTGRES_DBNAME}')
    metadata = MetaData()
    metadata.reflect(bind=engine)
    users = metadata.tables['users']
    conn = engine.connect()
    stmt = insert(users).values(
        name=name,
        username=username,
        password=password,
        email=email,
        user_field=user_field,
        years=years,
        country=country)
    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()

# %%
def create_admin_user(name, username, password, email, country):
    engine = create_engine(f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost/{POSTGRES_DBNAME}')
    metadata = MetaData()
    metadata.reflect(bind=engine)
    adm_users = metadata.tables['adm_users']
    conn = engine.connect()
    stmt = insert(adm_users).values(
    name=name,
    username=username,
    password=password,
    email=email,
    country=country)
    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()

# %%
def create_book(book_name, ISBN10,  author, content, field):
    book_id = uuid.uuid4()
    connection = MongoClient(f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@localhost", 27017)
    db = connection['data']
    mycol = db["Books"]

    book = { "book_id": f"{book_id}",
             "ISBN10": f"{ISBN10}",
             "book_name": f"{book_name}",
             "author": f"{author}",
             "content": f"{content}", 
             "field": f"{field}",   }

    mycol.insert_one(book)


def create_paper(paper_name,  author, content, field):
    paper_id = uuid.uuid4()
    connection = MongoClient(f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@localhost", 27017)
    db = connection['data']
    mycol = db["Papers"]

    paper = { "paper_id": f"{paper_id}",
             "paper_name": f"{paper_name}",
             "author": f"{author}",
             "content": f"{content}", 
             "field": f"{field}",   }

    mycol.insert_one(paper)

# %%
