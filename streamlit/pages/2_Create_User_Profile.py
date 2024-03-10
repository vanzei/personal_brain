# %%
import asyncio
import streamlit as st
from pydantic import BaseModel, validator, ValidationError, Field
import os
from dotenv import load_dotenv
import re
from script.transaction import create_user
from script.schema import User


st.set_page_config(page_title="Form Demo", page_icon="📊")


st.markdown("# Create User Profile")

async def process_form_data(fullname, my_username, my_pass, my_email, my_field, my_exp, my_country):
    # Ensure years is an integer
    try:
        my_exp = int(my_exp)
    except ValueError:
        st.error("Years of experience must be a number.")
        return None
    

    # Create User object
    user = User(name=fullname, username=my_username, password=my_pass, email=my_email, user_field=my_field, years=my_exp, country=my_country)
    return user

def run_async(coroutine):
    return asyncio.run(coroutine)

def main():
    with st.form("my_form"):
        st.write("Enter the User data")
        fullname = st.text_input("Full Name*", placeholder='Full Name')
        row = st.columns([1,1])
        my_username = row[0].text_input('Username *', placeholder='Name', help='Mandatory Field')
        my_pass = row[1].text_input('Password *', placeholder='Password', help='Mandatory Field', type='password')
        my_email = st.text_input('Email *', placeholder='Email', help='Mandatory Field')
        row1 = st.columns([1,1,1])
        my_exp = row1[0].text_input('Years of Experience *', placeholder='Experience', help='Inform how many years of experience')
        my_field = row1[1].text_input('Field *', placeholder='Field', help='SWE, Data, QA, etc')
        my_country = row1[2].text_input('Country *', placeholder='Country', help='Inform your country full name')
        submitted = st.form_submit_button('Create Profile')

        if submitted:
            
            try:
                user_data = run_async(process_form_data(fullname, my_username, my_pass, my_email, my_field, my_exp, my_country))
                if user_data:
                    st.success("Profile created successfully!")
                    create_user(fullname, my_username, my_pass, my_email, my_field, my_exp, my_country)
            except ValidationError as e:
                for error in e.errors():
                    st.error(f"{error['loc'][0]}: {error['msg']}")

if __name__ == '__main__':
    main()

# %%
