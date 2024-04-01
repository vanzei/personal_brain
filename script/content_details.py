# %%
from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)
# %%
def get_book_details(book_title, retry_count=5):
    value = book_title
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a senior software engineer with very humane knowledge from self-development books and MBA courses trying to suggest good content and summary books content."},
            {"role": "user", "content": 'Compose a book summary of the book ' + book_title + ' with at least 500 words and return ONLY the following json object format: [{"book_title": "title", "Authors":"{Book Authors}", "book_content": "summary", "ISBN10" : "ISBN10"}]'}
        ]
    )

    response = completion.choices[0].message
    book_data = None  # Initialize book_data to avoid reference before assignment
    try:
        book_data = json.loads(response.content)
    except json.decoder.JSONDecodeError:
        if retry_count > 0:
            return get_book_details(book_title, retry_count - 1)  # Retry with a decreased counter
        else:
            return {'book_title': 'Not Found', 'Authors': 'Not Found', 'book_content': "Not Found", 'ISBN10': 'Not Found'}
    return book_data
# %%
def get_paper_details(paper_name, retry_count=5):
    value = paper_name
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a senior software engineer with  very humane knowledge from self developtment books and MBA courses trying to suggest good content and sumamry books content."},
        {"role": "user", "content": 'Can you summarize the technical paper' + paper_name + ' and provide the key fundamental shared for further studies? The summary should contain at least 500 words and if you dont find the specific paper return the most similar one, sending in return ONLY the following json object format: [{"paper_title": "title", "Authors": "{Paper Authors}", "paper_content": "summary"}], do not apologize for not finding the correct document' }
    ]
    )

    response = completion.choices[0].message
    paper_data = None  # Initialize book_data to avoid reference before assignment
    try:
        paper_data = json.loads(response.content)
    except json.decoder.JSONDecodeError:
        if retry_count > 0:
            return get_paper_details(paper_name, retry_count - 1)  # Retry with a decreased counter
        else:
            return {'paper_title': 'Not Found', 'Authors': 'Not Found', 'paper_content': "Not Found"}
    return paper_data
# %%
