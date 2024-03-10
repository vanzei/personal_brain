import streamlit as st
from pydantic import BaseModel, ValidationError, Field
from dotenv import load_dotenv
import sys
import os

# Calculate the directory two levels up from the current script
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, '..', '..'))

# Add the parent directory to sys.path to make the script package importable
if parent_directory not in sys.path:
    sys.path.insert(0, parent_directory)

# Import create_paper from the script.transaction package
from script.transaction import create_paper
from script.content_details import get_paper_details

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

st.set_page_config(page_title="Form Demo", page_icon="📊")

class Paper(BaseModel):
    paper_name: str = Field(..., min_length=5)
    author: str
    content: str = Field(..., min_length=5)
    field: str

st.markdown("# Add Paper to the Brain 🤯🤯🤯")

def main():
    if 'paper_details' not in st.session_state:
        st.session_state.paper_details = {"paper_title": "", "Authors": "", "paper_content": "", "Paper Field": "Technology"}

    paper_name_input = st.text_input("Enter Paper Name*", placeholder='Book Name to Magic Complete😊', key='paper_name_input')
    find_content = st.button('Check Content: ✨🔎✨')

    # If "Check Content" is clicked and there's input, fetch and display paper details
    if find_content and paper_name_input:
        fetched_paper_details = get_paper_details(paper_name_input)
        print(fetched_paper_details)
        if fetched_paper_details:
            st.session_state.paper_details.update({
                "paper_title": fetched_paper_details[0].get('paper_title', ''),
                "Authors": fetched_paper_details[0].get('Authors', ''),
                "paper_content": fetched_paper_details[0].get('paper_content', ''),
                # Assuming you have a way to determine the field from fetched details
            })
        else:
            st.warning("No paper details found.")

    with st.form("my_form"):
        paper_name = st.text_input("Paper Name*", value=st.session_state.paper_details["paper_title"], key='paper_name')
        author = st.text_input('Author *', value=st.session_state.paper_details["Authors"], placeholder='Author', help='Mandatory Field', key='author')
        content = st.text_area('Paper Summary *', value=st.session_state.paper_details["paper_content"], placeholder='Paper Summary', help='Mandatory Field', key='content')
        field = st.selectbox('Book Field', ('Technology', 'Self Development', 'Data', 'Programming Language', 'System Design', 'Data Structure and Algorithms'), index=0, key='field')
        
        submitted = st.form_submit_button('Add PAper to the Brain!') 
        if submitted:
            try:
                paper_data = Paper(paper_name=paper_name, author=author, content=content, field=field)
                create_paper(paper_name, author, content, field)
                st.success("paper added successfully!")
                # Clear session state after successful submission if desired
                st.session_state.paper_details = {"paper_title": "", "Authors": "", "ISBN10": "", "paper_content": "", "paper Field": "Technology"}
            except ValidationError as e:
                for error in e.errors():
                    st.error(f"{error['loc'][0]}: {error['msg']}")

if __name__ == '__main__':
    main()
