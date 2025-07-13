import requests
from collections import Counter

# ------------------------------------------------------------------------------------

import pandas as pd

def dic_contest_submissions(s):

    ranges_s = len(s)

    dic_contest = {}  # contestId -> set of unique problem IDs
    dic_problem = {}  # problem ID -> verdicts, tags, rating, participant types

    for i in range(ranges_s):
        contest_id = s['contestId'].iloc[i]
        problem = s['problem'].iloc[i]
        problem_index = problem.get('index')
        problem_name = problem.get('name')
        problem_tags = problem.get('tags', [])
        problem_verdict = s['verdict'].iloc[i]
        problem_rating = problem.get('rating', None)
        participant_type = s['author'].iloc[i].get('participantType', '')

        problem_id = f"{contest_id}-{problem_index}"

        dic_contest.setdefault(contest_id, set()).add(problem_id)

        if problem_id in dic_problem:
            dic_problem[problem_id]['verdict'].append(problem_verdict)
            dic_problem[problem_id]['participantTypes'].add(participant_type)
        else:
            dic_problem[problem_id] = {
                'verdict': [problem_verdict],
                'tags': problem_tags,
                'rating': problem_rating,
                'name': problem_name,
                'contestId': contest_id,
                'index': problem_index,
                'participantTypes': {participant_type}
            }

    df_contest = pd.DataFrame([
        {"contestId": k, "problems": list(v)}
        for k, v in dic_contest.items()
    ])
    df_contest['Count_problems'] = df_contest['problems'].apply(len)

    df_problem = pd.DataFrame([
        {
            "problem_id": k,
            "verdicts": v['verdict'],
            "tags": v['tags'],
            "rating": v['rating'],
            "name": v['name'],
            "contestId": v['contestId'],
            "index": v['index'],
            "participantTypes": v['participantTypes']
        }
        for k, v in dic_problem.items()
    ])

    verdicts_correct = {'OK'}
    df_problem['Correct'] = df_problem['verdicts'].apply(
        lambda x: sum(v in verdicts_correct for v in x)
    )
    df_problem['TLE'] = df_problem['verdicts'].apply(lambda x: sum(v == 'TIME_LIMIT_EXCEEDED' for v in x))
    df_problem['MLE'] = df_problem['verdicts'].apply(lambda x: sum(v == 'MEMORY_LIMIT_EXCEEDED' for v in x))
    df_problem['Wrong'] = df_problem['verdicts'].apply(len) - df_problem['Correct'] - df_problem['TLE'] - df_problem['MLE']

    df_problem['IsContestant'] = df_problem['participantTypes'].apply(lambda x: int('CONTESTANT' in x))
    df_problem['IsVirtual'] = df_problem['participantTypes'].apply(lambda x: int('VIRTUAL' in x))

    df_problem.drop(columns=['verdicts', 'participantTypes'], inplace=True)

    df_unsolved = df_problem[df_problem['Correct'] == 0].copy()
    df_solved = df_problem[df_problem['Correct'] > 0].copy()

    return df_contest, df_problem, df_unsolved, df_solved




# -----------------------------------------------------------------------------------


def count_tags(df):
    all_tags = []
    for tags_list in df['tags']:
        if isinstance(tags_list, list):
            all_tags.extend(tags_list)

    tag_counts = Counter(all_tags)

    df_tags = pd.DataFrame([
        {"tag": tag, "count": count}
        for tag, count in tag_counts.items()
    ]).sort_values(by="count", ascending=False).reset_index(drop=True)

    return df_tags


#-------------------------------------------------------------------------------------------------------

def get_rating_counts(df):
    rating_counts = df['rating'].value_counts().reset_index()
    rating_counts.columns = ['rating', 'count']
    rating_counts = rating_counts.sort_values(by='rating')
    return rating_counts

#-------------------------------------------------------------------------------------------------------

def get_solved_during_contest(contest_id: int, handle: str) -> set:
    url = f"https://codeforces.com/api/contest.status?contestId={contest_id}&handle={handle}"
    r = requests.get(url)
    data = r.json()

    solved = set()

    if data['status'] != 'OK':
        return solved

    submissions = data['result']

    for sub in submissions:
        if sub['verdict'] == 'OK' and sub['author']['participantType'] == 'CONTESTANT':
            problem_index = sub['problem']['index']
            solved.add(f"{contest_id}-{problem_index}")

    return solved

#---------------------------------------------------------------------------------------------


def apply_dark_theme(fig, ax):

    fig.patch.set_facecolor('#111115')
    ax.set_facecolor('#111115')

    ax.grid(True, color='#333333')

    ax.title.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    for spine in ax.spines.values():
        spine.set_color('white')




