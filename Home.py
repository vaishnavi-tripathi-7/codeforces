import streamlit as st
import pandas as pd
import requests
from helper import dic_contest_submissions

st.set_page_config(
    page_title="Codeforces Analyzer",
    page_icon="💻",
    layout="wide"
)

left, right = st.columns(2)

with right:
    st.image("images/boy-coding-laptop.webp")

with left:
    st.markdown(
        "<h1 style='text-align: center;'>Codeforces Analyzer</h1>",
        unsafe_allow_html=True
    )
    st.write("")

    st.markdown(
        "<h3 style='text-align: center;'>Uncover your Codeforces stats like never before!</h3>",
        unsafe_allow_html=True
    )
    st.write("")

    st.write("""
    ✅ Analyze your submissions  
    ✅ Track your rating progress  
    ✅ See your strongest topics  
    """)


    st.write("")

    username = st.text_input("Enter your Codeforces username:", "")

    if not username:
        username = "tourist"

    st.session_state.username = username

    profile_url = f'https://codeforces.com/api/user.info?handles={username}'
    submission_url = f'https://codeforces.com/api/user.status?handle={username}'
    contest_url = f'https://codeforces.com/api/user.rating?handle={username}'

    prof = requests.get(profile_url).json()
    sub = requests.get(submission_url).json()
    con = requests.get(contest_url).json()

    st.session_state.present_rating = prof['result'][0]['rating']

    st.session_state.p = pd.DataFrame(prof['result'])
    s = pd.DataFrame(sub['result'])
    st.session_state.c = pd.DataFrame(con['result'])

    st.success(f"Data loaded for **{username}**! Go to the Analysis page ➡️")

    df_contest, df_problem, df_unsolved, df_solved = dic_contest_submissions(s)

    st.session_state.df_contest = df_contest
    st.session_state.df_problem = df_problem
    st.session_state.df_unsolved = df_unsolved
    st.session_state.df_solved = df_solved





