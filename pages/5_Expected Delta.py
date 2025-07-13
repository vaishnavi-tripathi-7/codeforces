import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import joblib

handle = st.session_state.get("username")

@st.cache_resource
def load_model():
    return joblib.load("cf_predictor.pkl")

model = load_model()

feature_order = [ 'contest_type', 'rating_before', 'rank', 'time_since_last', 'practice_days', 'practice_problems','practice_avg_rating' ]

st.title("Codeforces Next Rating Predictor")


if st.button("Predict"):
    try:

        r = requests.get(f"https://codeforces.com/api/user.rating?handle={handle}").json()
        if r['status'] != 'OK' or len(r['result']) < 2:
            st.error(f"Not enough contests for {handle}")
            st.stop()

        df_rating = pd.DataFrame(r['result']).sort_values("ratingUpdateTimeSeconds").reset_index(drop=True)

        s = requests.get(f"https://codeforces.com/api/user.status?handle={handle}").json()
        if s['status'] != 'OK':
            st.error(f"No submissions for {handle}")
            st.stop()

        df_subs = pd.DataFrame(s['result'])
        df_subs['participantType'] = df_subs['author'].apply(lambda x: x.get('participantType', 'UNKNOWN'))
        df_subs['time'] = pd.to_datetime(df_subs['creationTimeSeconds'], unit='s')

        last = df_rating.iloc[-1]
        prev = df_rating.iloc[-2]

        date_last = datetime.fromtimestamp(last['ratingUpdateTimeSeconds'])
        date_prev = datetime.fromtimestamp(prev['ratingUpdateTimeSeconds'])
        time_since_last = (datetime.now() - date_last).days

        practice = df_subs[ (df_subs['participantType'].isin(['PRACTICE', 'VIRTUAL'])) & (df_subs['time'] > date_last) ]

        practice_days = practice['time'].dt.date.nunique()
        practice_problems = practice['problem'].apply(  lambda x: f"{x.get('contestId', 'X')}-{x.get('index', 'X')}" ).nunique()

        ratings = practice['problem'].apply(lambda x: x.get('rating'))
        ratings = ratings.dropna()
        practice_avg_rating = ratings.mean() if not ratings.empty else 0

        name = last['contestName']
        if 'Div. 1' in name:
            contest_type = 1
        elif 'Div. 2' in name:
            contest_type = 2
        elif 'Div. 3' in name:
            contest_type = 3
        elif 'Educational' in name:
            contest_type = 4
        else:
            contest_type = 0

        rating_before = last['newRating']
        rank = last['rank']

        features = {
            'contest_type': contest_type,
            'rating_before': rating_before,
            'rank': rank,
            'time_since_last': time_since_last,
            'practice_days': practice_days,
            'practice_problems': practice_problems,
            'practice_avg_rating': practice_avg_rating
        }

        X = pd.DataFrame([[features[f] for f in feature_order]], columns=feature_order)

        st.subheader("Features for prediction")
        st.write(X)

        predicted_delta = model.predict(X)[0]
        predicted_delta = int(round(predicted_delta))
        predicted_next_rating = rating_before + predicted_delta

        st.success(f"Predicted delta for {handle}: {predicted_delta:+} points")
        st.success(f"Expected next rating: {predicted_next_rating}")

    except Exception as e:
        st.error(f"❌ Error: {e}")
