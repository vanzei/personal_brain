import asyncio
import streamlit as st
from pydantic import BaseModel, validator, ValidationError, Field
import os
from dotenv import load_dotenv
import re


import sys

# Calculate the directory two levels up from the current script
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, '..', '..'))

# Add the parent directory to sys.path to make the script package importable
if parent_directory not in sys.path:
    sys.path.insert(0, parent_directory)

from script.schema import AdminUser
from script.transaction import create_admin_user

load_dotenv()

ALLOWED_KEYS = os.getenv('ALLOWED_KEYS')




st.set_page_config(page_title="Form Demo", page_icon="📊")


st.markdown("# Create Admin User Profile")

async def process_form_data(fullname, my_username, my_pass, my_email, my_country, p_key):

    # Ensure years is an integer
    try:
        p_key = int(p_key)
    except ValueError:
        st.error("Key must be a number.")
        return None
        
    # Create AdminUser object
    user = AdminUser(name=fullname, username=my_username, password=my_pass, email=my_email, country=my_country, p_key = p_key)
    print(user)
    return user

def run_async(coroutine):
    return asyncio.run(coroutine)

def main():
    with st.form("my_form"):
        st.write("Enter the Admin User data")
        fullname = st.text_input('Username *', placeholder='Name', help='Mandatory Field')
        row = st.columns([1,1])
        my_username = row[0].text_input('Username *', key = 'user_name', placeholder='Name', help='Mandatory Field')
        my_pass = row[1].text_input('Password *', key = 'user_pass', placeholder='Password', help='Mandatory Field', type='password')   
        my_email = st.text_input('Email *', key = 'user_email', placeholder='Email', help='Mandatory Field')
        my_country = st.text_input('Country *', key = 'user_country', placeholder='Country', help='Inform your country full name')
        p_key = st.text_input("Enter your personal key", key = 'user_key', placeholder='Key')
        submitted = st.form_submit_button('Create Profile')

        if p_key in ALLOWED_KEYS:
            if submitted:

                try:
                    user_data = run_async(process_form_data(fullname, my_username, my_pass, my_email, my_country, p_key))
                    if user_data:
                        st.success("Profile created successfully!")
                        create_admin_user(fullname, my_username, my_pass, my_email, my_country)
                except ValidationError as e:
                    for error in e.errors():
                        st.error(f"{error['loc'][0]}: {error['msg']}")
        else:
            st.error("The Key doen't match a valid one!")

if __name__ == '__main__':
    main()
