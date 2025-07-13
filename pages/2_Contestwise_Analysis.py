import streamlit as st
from helper import get_solved_during_contest

df_problem = st.session_state.get("df_problem")
df_contest = st.session_state.get("df_contest")
c = st.session_state.get("c")
username = st.session_state.get("username")

if df_problem is None or username is None:
    st.error("❌ No data found. Please go back to the Home page and enter a username first.")
else:
    st.title("Contest Analysis")
    st.write("----")

    problem = df_problem.copy()
    contest = df_contest.copy()

    p = c.copy()
    p.drop(columns=['rank', 'handle', 'ratingUpdateTimeSeconds'], inplace=True, errors='ignore')

    for idx, row in p.iterrows():
        contest_number = idx + 1

        cid = row['contestId']
        cname = row['contestName'] if 'contestName' in row else f"Contest {cid}"
        old = row.get('oldRating', 'N/A')
        new = row.get('newRating', 'N/A')
        delta = int(new) - int(old)

        st.subheader(f"{contest_number}. {cname}")
        st.write(f"**Old Rating:** {old} → **New Rating:** {new}")
        st.write(f"**Delta:** {delta:+}")

        l = problem[problem['contestId'] == cid]

        solved_during_contest = get_solved_during_contest(cid, username)

        solved_overall = []
        dict_temp = {}

        for _, prob_row in l.iterrows():
            pid = prob_row['problem_id']
            pname = prob_row['name']
            prating = prob_row['rating']
            ptags = prob_row['tags']

            if isinstance(ptags, list):
                ptags = ", ".join(ptags)

            pcorrect = prob_row['Correct']
            patt = pcorrect + prob_row['Wrong'] + prob_row['TLE'] + prob_row['MLE']

            solved_overall.append(pid)

            dict_temp[pid] = {
                'name': pname,
                'rating': prating,
                'tags': ptags,
                'correct': pcorrect,
                'attempts': patt
            }

        # -----------------------------
        st.subheader("**→ Problems Solved During Contest:**")

        solved_during = [pid for pid in solved_overall if pid in solved_during_contest]

        if solved_during:
            left, middle, right = st.columns(3)
            cols = [left, middle, right]

            for idx, pid in enumerate(solved_during, start=1):
                col = cols[(idx % 3) - 1]
                with col:
                    d = dict_temp[pid]
                    st.markdown(
                        f"""
                        {idx}. **{d['name']}**  
                        • **Rating:** {d['rating']}  
                        • **Tags:** {d['tags']}  
                        • **Attempts:** {d['attempts']}
                        """
                    )
        else:
            st.info("None solved during contest.")

        # -----------------------------
        st.subheader("**→ Total Problems Solved:**")

        if solved_overall:
            left, middle, right = st.columns(3)
            cols = [left, middle, right]

            for idx, pid in enumerate(solved_overall, start=1):
                col = cols[(idx % 3) - 1]
                with col:
                    d = dict_temp[pid]
                    st.markdown(
                        f"""
                        {idx}. **{d['name']}**  
                        • **Rating:** {d['rating']}  
                        • **Tags:** {d['tags']}  
                        • **Attempts:** {d['attempts']}
                        """
                    )
        else:
            st.info("No problems attempted.")

        st.write("---")

    st.write("Contests over!")
