import streamlit as st
from helper import get_solved_during_contest

problem = st.session_state.get("df_problem")
contest = st.session_state.get("df_contest")
c = st.session_state.get("c")
username = st.session_state.get("username")

if problem is None or username is None:
    st.error("❌ No data found. Please go back to the Home page and enter a username first.")
else:
    st.title("Contest Analysis")
    st.write('----')
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
        st.write(f"**Old Rating:** {old} --→ **New Rating:** {new}  ")
        st.write(f'**Delta:** {delta:+}')

        l = problem[problem['contestId'] == cid]

        solved_during_contest = get_solved_during_contest(cid, username)

        solved_overall = []
        dict_temp = {}

        for _, prob_row in l.iterrows():
            pid = prob_row['problem_id']  # Format: contestId-Index
            pname = prob_row['name']
            prating = prob_row['rating']
            ptags = ", ".join(prob_row['tags'])
            pcorrect = prob_row['Correct']
            patt = prob_row['Correct'] + prob_row['Wrong'] + prob_row['TLE'] + prob_row['MLE']

            solved_overall.append(pid)

            dict_temp[pid] = {
                'name': pname,
                'rating': prating,
                'tags': ptags,
                'correct': pcorrect,
                'attempts': patt
            }

        st.subheader("**Problems Solved During Contest:**")
        solved_during = [pid for pid in solved_overall if pid in solved_during_contest]

        if solved_during:
            for idx, pid in enumerate(solved_during, start=1):
                d = dict_temp[pid]
                name = d['name']
                rating = d['rating']
                tags = ", ".join(d['tags']) if isinstance(d['tags'], list) else d['tags']
                attempts = d['attempts']
                st.markdown(
                    f"""
                    {idx}. **{name}**  
                      • **Rating:** {rating}  
                      • **Tags:** {tags}  
                      • **Attempts:** {attempts}
                    """
                )
        else:
            st.info("None solved during contest.")

        st.subheader("**Overall Problems Solved:**")
        if solved_overall:
            for idx, pid in enumerate(solved_overall, start=1):
                d = dict_temp[pid]
                name = d['name']
                rating = d['rating']
                tags = ", ".join(d['tags']) if isinstance(d['tags'], list) else d['tags']
                attempts = d['attempts']
                st.markdown(
                    f"""
                    {idx}. **{name}**  
                      • **Rating:** {rating}  
                      • **Tags:** {tags}  
                      • **Attempts:** {attempts}
                    """
                )
        else:
            st.info("No problems attempted.")

        st.write("---")


    st.write("Contests over !")



