import streamlit as st
import matplotlib.pyplot as plt
import datetime
import plotly.graph_objects as go
import seaborn as sns


username = st.session_state.get("username")
p = st.session_state.get("p")
c = st.session_state.get("c")

if p is None or c is None or username is None:
    st.warning(" No data found. Please go back to the Home page and enter your Codeforces handle.")
else:
    st.title(f"👋 Welcome : {username}")
    st.write("")

    # ---------------------------------------------------------------------------------------

    left, right = st.columns(2)

    with left:
        max_rating = p["maxRating"].iloc[0]
        max_rank = p["maxRank"].iloc[0]
        st.subheader(f"🏅 Max Rank: {max_rank}")
        st.subheader(f"📈 Max Rating: {max_rating}")

    with right:
        present_rating = p["rating"].iloc[0]
        present_rank = p["rank"].iloc[0]
        st.subheader(f"🎯 Current Rank: {present_rank}")
        st.subheader(f"⭐ Current Rating: {present_rating}")

    st.write("")

    st.write("----")

    # Add ratingChange
    c["ratingChange"] = c["newRating"] - c["oldRating"]
    # Number of contests
    num_contests = len(c)

    # ---------------------------------------------------------------------------------------

    # Best rank
    best_rank_row = c.loc[c["rank"].idxmin()]
    best_rank = best_rank_row["rank"]
    best_rank_contest_name = best_rank_row["contestName"]
    # Worst rank
    worst_rank_row = c.loc[c["rank"].idxmax()]
    worst_rank = worst_rank_row["rank"]
    worst_rank_contest_name = worst_rank_row["contestName"]
    # Max up
    max_up_row = c.loc[c["ratingChange"].idxmax()]
    max_up = max_up_row["ratingChange"]
    max_up_contest_name = max_up_row["contestName"]
    # Max down
    max_down_row = c.loc[c["ratingChange"].idxmin()]
    max_down = max_down_row["ratingChange"]
    max_down_contest_name = max_down_row["contestName"]
    # Display
    st.subheader("Contest Stats")
    st.write(f"**Number of contests:** {num_contests}")
    st.write(f"**Best rank:** {best_rank} ({best_rank_contest_name})")
    st.write(f"**Worst rank:** {worst_rank} ({worst_rank_contest_name})")
    st.write(f"**Max up:** {max_up} ({max_up_contest_name})")
    st.write(f"**Max down:** {max_down} ({max_down_contest_name})")
    st.write("")
    st.write("----")

    # ---------------------------------------------------------------------------------------

    st.subheader("Participation Graph")

    c_sorted = c.sort_values("ratingUpdateTimeSeconds")
    rating = c_sorted["newRating"].values
    contest_names = c_sorted["contestName"].values
    window_size = 50  # show 50 contests at a time
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=[], y=[], mode="lines+markers", line=dict(color="lime")))

    frames = []

    for i in range(len(rating)):
        if i < window_size:
            x_vals = list(range(i + 1))
            y_vals = rating[:i + 1]
            tick_labels = contest_names[:i + 1]
        else:
            x_vals = list(range(i - window_size + 1, i + 1))
            y_vals = rating[i - window_size + 1: i + 1]
            tick_labels = contest_names[i - window_size + 1: i + 1]

        frames.append(go.Frame(
            data=[go.Scatter(x=x_vals, y=y_vals, mode='lines+markers', line=dict(color='lime'))],
            layout=go.Layout( xaxis=dict(  tickmode='array', tickvals=x_vals, ticktext=tick_labels ) ) ))

    fig.frames = frames

    fig.update_layout( xaxis=dict( tickangle=-90,  tickmode='array',),showlegend=False,
        template="plotly_white", height=400, updatemenus=[dict( type="buttons", showactive=False,
            buttons=[ dict(label="▶ Play", method="animate",
                     args=[None, {"frame": {"duration": 200, "redraw": True}, "fromcurrent": True}])
            ], x=0.1, y=-0.15 )])

    st.plotly_chart(fig)
    st.write("----")

    # ---------------------------------------------------------------------------------------


    c_sorted = c.sort_values("ratingUpdateTimeSeconds", ascending=False)
    contest_data = c_sorted[["contestName", "newRating", "oldRating", "ratingChange", "rank"]]
    st.subheader("Contest History")
    st.write("")
    st.dataframe(contest_data , hide_index=True)

    # ---------------------------------------------------------------------------------------

    st.write("----")
    st.subheader(" Graph of delta increase and decrease ")
    st.write("")
    # Make sure 'date' exists
    if "date" not in c.columns:
        c["date"] = c["ratingUpdateTimeSeconds"].apply(
            lambda x: datetime.datetime.fromtimestamp(x)
        )
    c_sorted = c.sort_values("ratingUpdateTimeSeconds").reset_index()


    dates = c_sorted["date"]
    ratings = c_sorted["newRating"]
    fig1, ax1 = plt.subplots(figsize=(12, 3))

    for i in range(1, len(ratings)):
        x = [dates[i - 1], dates[i]]
        y = [ratings[i - 1], ratings[i]]
        if y[1] >= y[0]:
            color = "green"
        else:
            color = "red"
        ax1.plot(x, y, color=color, linewidth=2)

    plt.xticks(rotation=90)
    st.pyplot(fig1)
    st.write("")

    # ---------------------------------------------------------------------------------------
    st.write("----")
    st.write("")
    st.subheader("Rank Distribution")
    st.write("")
    fig, ax = plt.subplots(figsize=(12, 3))
    sns.histplot(c["rank"], bins=50, color="#8d988d", ax=ax)
    st.pyplot(fig)
    st.write("")

    # ---------------------------------------------------------------------------------------

    st.write("----")
    st.write("")
    st.subheader("Delta Change Over Time")
    st.write("")

    fig1, ax1 = plt.subplots(figsize=(12, 3))
    ax1.plot(c_sorted["date"], c["ratingChange"], marker=".", color='#66545e')
    st.pyplot(fig1)
    st.write("")

    # ---------------------------------------------------------------------------------------

    st.write("----")
    st.write("")
    st.subheader(" Rating overtime ")
    st.write("")

    if "date" not in c.columns:
        c["date"] = c["ratingUpdateTimeSeconds"].apply(
            lambda x: datetime.datetime.fromtimestamp(x)
        )

    c_sorted = c.sort_values("ratingUpdateTimeSeconds")
    fig1, ax1 = plt.subplots(figsize=(12, 3))
    ax1.plot(c_sorted["date"], c_sorted["newRating"], marker=".", color='#aa6f73')
    st.pyplot(fig1)
    st.write("")

    # ---------------------------------------------------------------------------------------









