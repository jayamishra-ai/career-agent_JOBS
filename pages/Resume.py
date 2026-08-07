import streamlit as st
from Database.supabase_service import get_profiles
import os
from dotenv import load_dotenv

load_dotenv()

st.write(os.getenv("SUPABASE_URL"))
st.title("My Profile")

response = get_profiles()

if response.data:

    profile = response.data[0]

    st.subheader(profile["name"])

    st.write("Skills:")
    st.write(profile["skills"])

    st.write("Target Roles:")
    st.write(profile["roles"])