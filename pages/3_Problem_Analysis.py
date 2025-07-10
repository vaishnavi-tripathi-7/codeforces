import streamlit as st
import matplotlib.pyplot as plt

from helper import count_tags , get_rating_counts
import seaborn as sns

unsolved = st.session_state.get("df_unsolved")
solved =  st.session_state.get("df_solved")
problem = st.session_state.get("df_problem")


if  unsolved is None :
    st.error("❌ No data found. Please go back to the Home page and enter a username first.")
else:

    #-------------------------------------------------------------------------

    st.title("Problem Analysis ")
    st.write("")

    problem_df = problem
    solved_df = solved

    tried = problem_df.shape[0]
    solved_count = solved_df.shape[0]

    solved_df['Attempts'] = solved_df[['Correct', 'TLE', 'MLE', 'Wrong']].sum(axis=1)
    avg_attempts = solved_df['Attempts'].mean()

    max_attempts_df = problem_df.copy()
    max_attempts_df['Attempts'] = max_attempts_df[['Correct', 'TLE', 'MLE', 'Wrong']].sum(axis=1)

    max_attempts_value = max_attempts_df['Attempts'].max()
    max_attempts_problem = max_attempts_df.loc[max_attempts_df['Attempts'].idxmax(), 'name']

    one_shot_solved = solved_df[(solved_df['Correct'] == 1) & (solved_df['TLE'] == 0) & (solved_df['MLE'] == 0 )& (solved_df['Wrong'] == 0) ].shape[0]
    one_shot_percent = 100 * one_shot_solved / solved_count if solved_count else 0

    max_ac_value = problem_df['Correct'].max()
    max_ac_problems = problem_df[problem_df['Correct'] == max_ac_value]['name'].tolist()

    st.write(f"Tried: {tried}")
    st.write(f"Solved: {solved_count}")
    st.write(f"Average attempts: {avg_attempts:.2f}")
    st.write(f"Max attempts: {max_attempts_value} ({max_attempts_problem})")
    st.write(f"Solved with one submission: {one_shot_solved} ({one_shot_percent:.2f}%)")
    st.write(f"Max AC(s): {max_ac_value} for problem(s): {max_ac_problems}")
    st.write("")

    #-------------------------------------------------------------------------------

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

    # ----------------------------------------------------------------------------------

    st.write("----")
    st.write("")
    st.subheader("Distribution of Solved Questions:")
    st.write("")

    rating_count = get_rating_counts(solved)
    rating_count['color'] = rating_count['rating'].apply(get_cf_color)

    fig, ax = plt.subplots(figsize=(10, 3))
    sns.barplot( data=rating_count, x='rating', y='count', ax=ax, palette=rating_count['color'].tolist()  )

    plt.xticks(rotation=90)
    ax.set_xlabel("Rating")
    ax.set_ylabel("Count")
    st.pyplot(fig)
    st.write("")

    # --------------------------------------------

    st.write("----")
    st.write("")
    st.subheader("Distribution of Unsolved Questions:")
    st.write("")


    rating_count = get_rating_counts(unsolved)
    rating_count['color'] = rating_count['rating'].apply(get_cf_color)

    fig, ax = plt.subplots(figsize=(10, 3))
    sns.barplot( data=rating_count, x='rating', y='count', ax=ax,  palette=rating_count['color'].tolist()   )
    plt.xticks(rotation=90)
    ax.set_xlabel("Rating")
    ax.set_ylabel("Count")
    st.pyplot(fig)
    st.write("")

    #----------------------------------------------------------------------------------------------

    st.write("----")
    st.write("")
    st.subheader("Overall Verdict Distribution  ")
    st.write("")

    left, right = st.columns(2)

    with right:
        st.write("For Unsolved Questions ")
        df = unsolved
        verdict_counts = {'TLE': df['TLE'].sum(),
                          'MLE': df['MLE'].sum(), 'Wrong': df['Wrong'].sum(), }

        labels = list(verdict_counts.keys())
        sizes = list(verdict_counts.values())

        fig, ax = plt.subplots(figsize=(5, 5))
        colors = sns.color_palette('pastel')[0:len(labels)]
        ax.pie(sizes, autopct='%1.1f%%', colors=colors, startangle=90, radius=1)
        ax.legend(labels, title="Verdicts", loc="upper center", bbox_to_anchor=(1.5, 1),
                  prop={'size': 8}, title_fontsize='10')
        st.pyplot(fig)

    with left:
        st.write("For solved Questions ")
        df = solved
        verdict_counts = {'Correct': df['Correct'].sum(), 'TLE': df['TLE'].sum(),
                          'MLE': df['MLE'].sum(), 'Wrong': df['Wrong'].sum(), }

        labels = list(verdict_counts.keys())
        sizes = list(verdict_counts.values())

        fig, ax = plt.subplots(figsize=(5, 5))
        colors = sns.color_palette('pastel')[0:len(labels)]
        ax.pie(sizes, autopct='%1.1f%%', colors=colors, startangle=90, radius=1)
        ax.legend(labels, title="Verdicts", loc="upper center", bbox_to_anchor=(1.5, 1),
                  prop={'size': 8}, title_fontsize='10')
        st.pyplot(fig)
    st.write("")

    # --------------------------------------------------------------------------------------


    tags_solved = count_tags(solved)
    tags_unsolved = count_tags(unsolved)
    st.session_state.tags_solved = tags_solved

    df = tags_solved

    st.write("----")
    st.write("")
    st.subheader("Tags for Solved Questions:")
    st.write("")

    fig, ax = plt.subplots(figsize=(15, 3))
    ax.pie(df['count'], colors=sns.color_palette('pastel')[0:len(df)], radius=1)
    ax.legend(df['tag'], title="Tags", loc="upper center", bbox_to_anchor=(2, 1),
              prop={'size': 8}, title_fontsize='10' , ncols=2)
    st.pyplot(fig)
    st.write("")



    #--------------------------------------------------------------------------------------

    st.write("----")
    st.write("")
    st.subheader("Unsolved Questions List along with their Tags & Links:")
    st.write("")

    flat_df = unsolved[['name', 'tags', 'contestId', 'index']].dropna()
    flat_df.rename(columns={'name': 'Problem Name'}, inplace=True)
    flat_df['Link'] = flat_df.apply(
        lambda row: f"https://codeforces.com/contest/{row['contestId']}/problem/{row['index']}",
        axis=1
    )
    st.dataframe(flat_df[['Problem Name', 'tags', 'Link']], hide_index=True)

    # ----------------------------------------------------------------------------------



    # --------------------------------------------------------------------------------------


    # --------------------------------------------------------------------------------------


    # --------------------------------------------------------------------------------------

    #--------------------------------------------------------------------------------------



