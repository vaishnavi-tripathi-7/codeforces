import streamlit as st
import requests
import pandas as pd
from helper import dic_contest_submissions , get_rating_counts ,count_tags , apply_dark_theme
import matplotlib.pyplot as plt
import seaborn as sns
import datetime


#---------------------------------------------------------------------------------------------------

unsolved1 = (st.session_state.get("df_unsolved")).copy()
solved1 = (st.session_state.get("df_solved")).copy()
problem1 = (st.session_state.get("df_problem")).copy()
p1 = (st.session_state.get("p")).copy()
username = st.session_state.get("username")
c1 = (st.session_state.get("c")).copy()



st.sidebar.header("Compare with another Codeforces user")
second_handle = st.sidebar.text_input("Enter second Codeforces ID:")

if not second_handle:
    st.info("Enter a second handle in the sidebar to compare.")

else:

    st.title( "Comparison Analysis")
    st.write("----")

    submission_url = f"https://codeforces.com/api/user.status?handle={second_handle}"
    info_url = f"https://codeforces.com/api/user.info?handles={second_handle}"
    contest_url = f"https://codeforces.com/api/user.rating?handle={second_handle}"
    submission_response = requests.get(submission_url).json()
    info_response = requests.get(info_url).json()
    contest_response = requests.get(contest_url).json()

    s2 = pd.DataFrame(submission_response['result'])
    p2 = pd.DataFrame(info_response['result'])
    c2 = pd.DataFrame(contest_response['result'])

    df_contest2, problem2, unsolved2, solved2 = dic_contest_submissions(s2)

    if (contest_response['status'] != 'OK') or (info_response['status'] != 'OK') or (submission_response['status'] != 'OK')  :
        st.error(f"Could not fetch contest history for '{second_handle}'.")
        st.stop()

    #----------------------------------------------------------------------------------------------


    left_col, right_col = st.columns(2)
    # ----------------------------
    with left_col:
        st.subheader(f"{username}")
        st.subheader("🔹 Rank & Rating")
        st.write(f"🏅 Max Rank: {p1['maxRank'].iloc[0]}")
        st.write(f"📈 Max Rating: {p1['maxRating'].iloc[0]}")
        st.write(f"🎯 Current Rank: {p1['rank'].iloc[0]}")
        st.write(f"⭐ Current Rating: {p1['rating'].iloc[0]}")

        # Contest stats
        c1["ratingChange"] = c1["newRating"] - c1["oldRating"]
        st.subheader("🏆 Contest Stats")
        st.write(f"Contests: {len(c1)}")
        st.write(f"Best rank: {c1.loc[c1['rank'].idxmin(), 'rank']} ({c1.loc[c1['rank'].idxmin(), 'contestName']})")
        st.write(f"Worst rank: {c1.loc[c1['rank'].idxmax(), 'rank']} ({c1.loc[c1['rank'].idxmax(), 'contestName']})")
        st.write(f"Max up: {c1['ratingChange'].max()} ({c1.loc[c1['ratingChange'].idxmax(), 'contestName']})")
        st.write(f"Max down: {c1['ratingChange'].min()} ({c1.loc[c1['ratingChange'].idxmin(), 'contestName']})")

        # Problem stats
        st.subheader("📚 Problem Stats")
        solved1['Attempts'] = solved1[['Correct', 'TLE', 'MLE', 'Wrong']].sum(axis=1)
        avg_attempts1 = solved1['Attempts'].mean()

        max_attempts_df1 = problem1.copy()
        max_attempts_df1['Attempts'] = max_attempts_df1[['Correct', 'TLE', 'MLE', 'Wrong']].sum(axis=1)

        st.write(f"Tried: {problem1.shape[0]}")
        st.write(f"Solved: {solved1.shape[0]}")
        st.write(f"Avg Attempts: {avg_attempts1:.2f}")
        st.write(f"Max Attempts: {max_attempts_df1['Attempts'].max()} ({max_attempts_df1.loc[max_attempts_df1['Attempts'].idxmax(), 'name']})")

        one_shot1 = solved1[
            (solved1['Correct'] == 1) &
            (solved1['TLE'] == 0) &
            (solved1['MLE'] == 0) &
            (solved1['Wrong'] == 0)
        ].shape[0]

        st.write(f"One-shot solved: {one_shot1}")
        st.write(f"Most ACs: {problem1['Correct'].max()}")

    # ----------------------------
    with right_col:
        st.subheader(f" {second_handle}")
        st.subheader("🔹 Rank & Rating")
        st.write(f"🏅 Max Rank: {p2['maxRank'].iloc[0]}")
        st.write(f"📈 Max Rating: {p2['maxRating'].iloc[0]}")
        st.write(f"🎯 Current Rank: {p2['rank'].iloc[0]}")
        st.write(f"⭐ Current Rating: {p2['rating'].iloc[0]}")

        # Contest stats
        c2["ratingChange"] = c2["newRating"] - c2["oldRating"]
        st.subheader("🏆 Contest Stats")
        st.write(f"Contests: {len(c2)}")
        st.write(f"Best rank: {c2.loc[c2['rank'].idxmin(), 'rank']} ({c2.loc[c2['rank'].idxmin(), 'contestName']})")
        st.write(f"Worst rank: {c2.loc[c2['rank'].idxmax(), 'rank']} ({c2.loc[c2['rank'].idxmax(), 'contestName']})")
        st.write(f"Max up: {c2['ratingChange'].max()} ({c2.loc[c2['ratingChange'].idxmax(), 'contestName']})")
        st.write(f"Max down: {c2['ratingChange'].min()} ({c2.loc[c2['ratingChange'].idxmin(), 'contestName']})")

        # Problem stats
        st.subheader("📚 Problem Stats")
        solved2['Attempts'] = solved2[['Correct', 'TLE', 'MLE', 'Wrong']].sum(axis=1)
        avg_attempts2 = solved2['Attempts'].mean()

        max_attempts_df2 = problem2.copy()
        max_attempts_df2['Attempts'] = max_attempts_df2[['Correct', 'TLE', 'MLE', 'Wrong']].sum(axis=1)

        st.write(f"Tried: {problem2.shape[0]}")
        st.write(f"Solved: {solved2.shape[0]}")
        st.write(f"Avg Attempts: {avg_attempts2:.2f}")
        st.write(f"Max Attempts: {max_attempts_df2['Attempts'].max()} ({max_attempts_df2.loc[max_attempts_df2['Attempts'].idxmax(), 'name']})")

        one_shot2 = solved2[
            (solved2['Correct'] == 1) &
            (solved2['TLE'] == 0) &
            (solved2['MLE'] == 0) &
            (solved2['Wrong'] == 0)
        ].shape[0]

        st.write(f"One-shot solved: {one_shot2}")
        st.write(f"Most ACs: {problem2['Correct'].max()}")

    #-----------------------------------------------------------------------------------------

    st.write("----")
    st.write("")
    st.subheader("Rank Distribution Comparison")
    st.write("")
    fig, ax = plt.subplots(figsize=(12, 4))
    sns.histplot(c1["rank"], bins=50, color="#9F63C4", label=f"{username}", kde=False, alpha=0.6, ax=ax )
    sns.histplot(c2["rank"], bins=50, color="#E2BAB1", label=f"{second_handle}", kde=False, alpha=0.7, ax=ax)
    ax.legend()
    apply_dark_theme(fig, ax)
    ax.grid(False)
    st.pyplot(fig)

    #----------------------------------------------------------------------------------------------

    st.write("----")
    st.write("")
    st.subheader("Rating Over Time")
    st.write("")

    if "date" not in c1.columns:
        c1["date"] = c1["ratingUpdateTimeSeconds"].apply(
            lambda x: datetime.datetime.fromtimestamp(x)
        )
    if "date" not in c2.columns:
        c2["date"] = c2["ratingUpdateTimeSeconds"].apply(
            lambda x: datetime.datetime.fromtimestamp(x)
        )

    c1_sorted = c1.sort_values("ratingUpdateTimeSeconds")
    c2_sorted = c2.sort_values("ratingUpdateTimeSeconds")

    fig2, ax2 = plt.subplots(figsize=(12, 4))
    ax2.plot(c1_sorted["date"], c1_sorted["newRating"], marker=".", color="#9F63C4", label=username)
    ax2.plot(c2_sorted["date"], c2_sorted["newRating"], marker=".", color="#E2BAB1", label=second_handle)
    ax2.legend()
    apply_dark_theme(fig2, ax2)
    st.pyplot(fig2)

    #----------------------------------------------------------------------------------------------

    def get_cf_color(rating):
        if rating < 1200:
            return "#808080"  # gray
        elif rating < 1400:
            return "#008000"  # green
        elif rating < 1600:
            return "#03A89E"  # cyan
        elif rating < 1900:
            return "#0000FF"  # blue
        elif rating < 2100:
            return "#AA00AA"  # violet
        elif rating < 2300:
            return "#FF8C00"  # orange
        else:
            return "#FF0000"  # red

    st.write("----")
    st.write("")
    st.subheader("Distribution of Solved Questions by Rating")
    st.write("")

    left_col, right_col = st.columns(2)

    with left_col:
        st.markdown(f"### {username}")
        rating_count1 = get_rating_counts(solved1)
        rating_count1['color'] = rating_count1['rating'].apply(get_cf_color)

        fig1, ax1 = plt.subplots(figsize=(8, 3))
        sns.barplot( data=rating_count1, x='rating', y='count', palette=rating_count1['color'].tolist(), ax=ax1)
        plt.xticks(rotation=90)
        apply_dark_theme(fig1, ax1)
        ax1.grid(False)
        st.pyplot(fig1)

    with right_col:
        st.markdown(f"### {second_handle}")
        rating_count2 = get_rating_counts(solved2)
        rating_count2['color'] = rating_count2['rating'].apply(get_cf_color)

        fig2, ax2 = plt.subplots(figsize=(8, 3))
        sns.barplot( data=rating_count2, x='rating', y='count', palette=rating_count2['color'].tolist(), ax=ax2)
        plt.xticks(rotation=90)
        apply_dark_theme(fig2, ax2)
        ax2.grid(False)
        st.pyplot(fig2)


    #----------------------------------------------------------------------------------------------

    st.write("----")
    st.write("")
    st.subheader("Solved Questions Verdict Breakdown")
    st.write("")

    left_col, right_col = st.columns(2)

    with left_col:
        st.markdown(f"### {username}")
        df1 = solved1.copy()
        verdict_counts1 = { 'AC' : df1['Correct'].sum() ,'TLE': df1['TLE'].sum(), 'MLE': df1['MLE'].sum(), 'Wrong': df1['Wrong'].sum()}

        labels1 = list(verdict_counts1.keys())
        sizes1 = list(verdict_counts1.values())

        fig1, ax1 = plt.subplots(figsize=(5, 5))
        colors1 = sns.color_palette('pastel')[0:len(labels1)]

        ax1.pie( sizes1, autopct='%1.1f%%', colors=colors1, startangle=90, radius=1 )
        ax1.legend( labels1, title="Verdicts", loc="upper center", bbox_to_anchor=(1.3, 1), prop={'size': 8}, title_fontsize='10')
        apply_dark_theme(fig1, ax1)
        st.pyplot(fig1)

    with right_col:
        st.markdown(f"### {second_handle}")
        df2 = solved2.copy()
        verdict_counts2 = { 'AC' : df2['Correct'].sum() ,'TLE': df2['TLE'].sum(),'MLE': df2['MLE'].sum(),'Wrong': df2['Wrong'].sum()}

        labels2 = list(verdict_counts2.keys())
        sizes2 = list(verdict_counts2.values())

        fig2, ax2 = plt.subplots(figsize=(5, 5))
        colors2 = sns.color_palette('pastel')[0:len(labels2)]

        ax2.pie( sizes2,  autopct='%1.1f%%',  colors=colors2, startangle=90, radius=1 )
        ax2.legend( labels2, title="Verdicts", loc="upper center", bbox_to_anchor=(1.3, 1),prop={'size': 8}, title_fontsize='10')
        apply_dark_theme(fig2, ax2)
        st.pyplot(fig2)


    #----------------------------------------------------------------------------------------------

    tags_solved1 = count_tags(solved1)
    tags_solved2 = count_tags(solved2)

    st.write("----")
    st.write("")
    st.subheader("Tags for Solved Questions")
    st.write("")

    st.markdown(f"### {username}")
    df1 = tags_solved1.copy()
    fig1, ax1 = plt.subplots(figsize=(15, 3))
    ax1.pie( df1['count'], colors=sns.color_palette('pastel')[0:len(df1)], radius=1,  startangle=90 )
    ax1.legend( df1['tag'], title="Tags", loc="upper center", bbox_to_anchor=(2, 1), prop={'size': 8}, title_fontsize='10', ncols=2 )
    apply_dark_theme(fig1, ax1)
    st.pyplot(fig1)

    st.markdown(f"### {second_handle}")
    df2 = tags_solved2.copy()
    fig2, ax2 = plt.subplots(figsize=(15, 3))
    ax2.pie( df2['count'], colors=sns.color_palette('pastel')[0:len(df2)], radius=1, startangle=90)
    ax2.legend( df2['tag'], title="Tags", loc="upper center", bbox_to_anchor=(2, 1), prop={'size': 8}, title_fontsize='10', ncols=2)
    apply_dark_theme(fig2, ax2)
    st.pyplot(fig2)

    st.write("----")

    #----------------------------------------------------------------------------------------------

    #----------------------------------------------------------------------------------------------

    #----------------------------------------------------------------------------------------------

    #----------------------------------------------------------------------------------------------



