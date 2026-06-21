import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from db import (
    get_total_users,
    get_total_analyses,
    get_popular_personality,
    get_user_history,
    fetch_query
)

# ==========================
# STUDENT DASHBOARD
# ==========================

def student_dashboard():

    st.title("📊 Student Dashboard")

    username = st.session_state.username

    history = get_user_history(username)

    if len(history) == 0:
        st.warning("No analysis history found.")
        return

    df = pd.DataFrame(history)

    st.subheader("📜 Analysis History")

    st.dataframe(df)

    st.subheader("🎯 Personality Distribution")

    personality_counts = (
        df["personality"]
        .value_counts()
    )

    fig, ax = plt.subplots()

    ax.pie(
        personality_counts,
        labels=personality_counts.index,
        autopct="%1.1f%%"
    )

    st.pyplot(fig)

    st.subheader("📈 Score Trend")

    st.line_chart(df["score"])

# ==========================
# ADMIN DASHBOARD
# ==========================

def admin_dashboard():

    st.title("🛠 Admin Dashboard")

    total_users = get_total_users()
    total_analyses = get_total_analyses()
    popular = get_popular_personality()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "👥 Total Users",
        total_users
    )

    col2.metric(
        "🎵 Total Analyses",
        total_analyses
    )

    col3.metric(
        "🏆 Popular Personality",
        popular
    )

    st.markdown("---")

    # ======================
    # ALL USERS
    # ======================

    users_query = """
    SELECT
    username,
    email,
    role,
    created_at
    FROM users
    """

    users = fetch_query(users_query)

    users_df = pd.DataFrame(users)

    st.subheader("👤 Registered Users")

    st.dataframe(users_df)

    # ======================
    # ALL RESULTS
    # ======================

    results_query = """
    SELECT *
    FROM results
    """

    results = fetch_query(results_query)

    if len(results) == 0:
        st.warning("No results available")
        return

    results_df = pd.DataFrame(results)

    st.subheader("📊 Analysis Records")

    st.dataframe(results_df)

    # ======================
    # BAR CHART
    # ======================

    st.subheader("🎯 Personality Popularity")

    personality_chart = (
        results_df["personality"]
        .value_counts()
    )

    st.bar_chart(personality_chart)

    # ======================
    # PIE CHART
    # ======================

    st.subheader("🥧 Personality Distribution")

    fig, ax = plt.subplots()

    ax.pie(
        personality_chart,
        labels=personality_chart.index,
        autopct="%1.1f%%"
    )

    st.pyplot(fig)

    # ======================
    # GENRE ANALYSIS
    # ======================

    st.subheader("🎧 Genre Popularity")

    genre_chart = (
        results_df["genre"]
        .value_counts()
    )

    st.bar_chart(genre_chart)

# ==========================
# USER SEARCH
# ==========================

def search_user():

    st.subheader("🔍 Search User")

    username = st.text_input(
        "Enter Username"
    )

    if st.button("Search"):

        query = """
        SELECT *
        FROM results
        WHERE username=%s
        """

        result = fetch_query(
            query,
            (username,)
        )

        if len(result) == 0:

            st.error(
                "No records found"
            )

        else:

            st.dataframe(
                pd.DataFrame(result)
            )