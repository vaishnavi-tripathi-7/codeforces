import streamlit as st
import requests
import pandas as pd

df_solved = st.session_state.get("df_solved")
tags_solved = st.session_state.get("tags_solved")
present_rating = st.session_state.get("present_rating")

if tags_solved is None or df_solved is None or present_rating is None:
    st.error("❌ No data found. Please go back to the Home page and enter a username first.")
else:
    st.title("📊 Problem Recommendations")

    tags_solved = tags_solved.sort_values('count')
    weak_tags = tags_solved.tail(10)['tag'].unique()

    def has_weak_tag(tags_list):
        return any(tag in weak_tags for tag in tags_list)

    min_limit = present_rating - 200
    max_limit = present_rating + 300

    solved_problem_ids = set(df_solved['problem_id'].unique())


    url = "https://codeforces.com/api/problemset.problems"

    try:
        response = requests.get(url)
        data = response.json()

        if data['status'] == 'OK':
            problems = data['result']['problems']
            df = pd.DataFrame(problems)
            df = df[df['rating'].notnull()]
            df['problem_id'] = df['contestId'].astype(str) + "-" + df['index']
            df['tags'] = df['tags'].apply(lambda x: x if isinstance(x, list) else [])

            df_filtered = df[
                (df['rating'] >= min_limit) &
                (df['rating'] <= max_limit) &
                (df['tags'].apply(has_weak_tag)) &
                (~df['problem_id'].isin(solved_problem_ids))
            ].drop_duplicates('problem_id').head(20)

            if not df_filtered.empty:
                for _, row in df_filtered.iterrows():
                    name = row['name']
                    rating = row['rating']
                    tags = ", ".join(row['tags'])
                    cid = row['contestId']
                    index = row['index']
                    link = f"https://codeforces.com/contest/{cid}/problem/{index}"
                    st.markdown(f"- [{name}]({link}) — Rating: {rating}, Tags: {tags}")

            else:
                st.warning("⚠️ No problems found in the given range and tags.")
        else:
            st.error("🚨 Could not fetch problems from Codeforces API. Try again later!")

    except Exception as e:
        st.error(f"🚨 Error while fetching from Codeforces API: {e}")










