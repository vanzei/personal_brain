import streamlit as st
from pydantic import BaseModel, ValidationError, Field
from dotenv import load_dotenv

import os
import sys

# Calculate the directory two levels up from the current script
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, '..', '..'))

# Add the parent directory to sys.path to make the script package importable
if parent_directory not in sys.path:
    sys.path.insert(0, parent_directory)

# Import create_paper from the script.transaction package
from script.transaction import create_book
from script.content_details import get_book_details

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

st.set_page_config(page_title="Form Demo", page_icon="📊")

class Book(BaseModel):
    ISBN10: str
    book_name: str = Field(..., min_length=5)
    author: str
    content: str = Field(..., min_length=5)
    field: str

st.markdown("# Add Book to the Brain 🤯🤯🤯")

def main():
    if 'book_details' not in st.session_state:
        st.session_state.book_details = {"book_title": "", "Authors": "", "ISBN10": "", "book_content": "", "Book Field": "Technology"}

    book_name_input = st.text_input("Enter Book Name*", placeholder='Book Name to Magic Complete😊', key='book_name_input')
    find_content = st.button('Check Content: ✨🔎✨')

    # If "Check Content" is clicked and there's input, fetch and display book details
    if find_content and book_name_input:
        fetched_book_details = get_book_details(book_name_input)
        if fetched_book_details:
            st.session_state.book_details.update({
                "book_title": fetched_book_details[0].get('book_title', ''),
                "Authors": fetched_book_details[0].get('Authors', ''),
                "ISBN10": fetched_book_details[0].get('ISBN10', ''),
                "book_content": fetched_book_details[0].get('book_content', ''),
                # Assuming you have a way to determine the field from fetched details
            })
        else:
            st.warning("No book details found.")

    with st.form("my_form"):
        book_name = st.text_input("Book Name*", value=st.session_state.book_details["book_title"], key='book_name')
        author = st.text_input('Author *', value=st.session_state.book_details["Authors"], placeholder='Author', help='Mandatory Field', key='author')
        ISBN10 = st.text_input('ISBN10 *', value=st.session_state.book_details["ISBN10"], placeholder='ISBN10', help='Mandatory Field', key='ISBN10')
        content = st.text_area('Book Summary *', value=st.session_state.book_details["book_content"], placeholder='Book Summary', help='Mandatory Field', key='content')
        field = st.selectbox('Book Field', ('Technology', 'Self Development', 'Data', 'Programming Language', 'System Design', 'Data Structure and Algorithms'), index=0, key='field')
        
        submitted = st.form_submit_button('Add Book to the Brain!') 
        if submitted:
            try:
                book_data = Book(book_name=book_name, ISBN10=ISBN10, author=author, content=content, field=field)
                create_book(book_name, ISBN10, author, content, field)
                st.success("Book added successfully!")
                # Clear session state after successful submission if desired
                st.session_state.book_details = {"book_title": "", "Authors": "", "ISBN10": "", "book_content": "", "Book Field": "Technology"}
            except ValidationError as e:
                for error in e.errors():
                    st.error(f"{error['loc'][0]}: {error['msg']}")

if __name__ == '__main__':
    main()
