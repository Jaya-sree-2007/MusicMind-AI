# ============================================
# MUSICMIND AI - PART 1
# Authentication + MySQL + Session Management
# ============================================

import streamlit as st
import mysql.connector
import bcrypt
import random
import string
from datetime import datetime

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="MusicMind AI",
    page_icon="🎧",
    layout="wide"
)

# ============================================
# PREMIUM UI
# ============================================

st.markdown("""
<style>

.stApp{
background: linear-gradient(
135deg,
#667eea 0%,
#764ba2 100%
);
}

.main .block-container{
background: rgba(255,255,255,0.15);
backdrop-filter: blur(12px);
padding:2rem;
border-radius:25px;
}

h1,h2,h3,label,p{
color:white !important;
}

.stButton>button{
width:100%;
background:#1DB954;
color:white;
border:none;
border-radius:12px;
font-weight:bold;
}

.stTextInput input{
border-radius:12px;
}

</style>
""", unsafe_allow_html=True)

# ============================================
# MYSQL CONNECTION
# ============================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Jaya@2007",      # <-- Put your password here
    "database": "musicmind_ai"
}

# ============================================
# CONNECT DATABASE
# ============================================

def get_connection():

    try:

        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        )

        return conn

    except Exception as e:

        st.error(f"Database Error: {e}")

        return None

# ============================================
# CREATE TABLES
# ============================================

def create_tables():

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS users(

        id INT AUTO_INCREMENT PRIMARY KEY,

        username VARCHAR(100) UNIQUE,

        email VARCHAR(200),

        password VARCHAR(255),

        role VARCHAR(20),

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS results(

        id INT AUTO_INCREMENT PRIMARY KEY,

        username VARCHAR(100),

        personality VARCHAR(100),

        genre VARCHAR(100),

        score INT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    conn.commit()

    cursor.close()

    conn.close()

create_tables()

# ============================================
# SESSION VARIABLES
# ============================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

if "otp" not in st.session_state:
    st.session_state.otp = ""

# ============================================
# GENERATE OTP
# ============================================

def generate_otp():

    otp = ''.join(
        random.choices(
            string.digits,
            k=6
        )
    )

    return otp

# ============================================
# SIGNUP
# ============================================

def signup_page():

    st.header("📝 Create Account")

    username = st.text_input(
        "Username",
        key="signup_user"
    )

    email = st.text_input(
        "Email",
        key="signup_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="signup_pass"
    )

    role = st.selectbox(
        "Role",
        [
            "student",
            "admin"
        ]
    )

    if st.button(
        "Create Account",
        key="signup_btn"
    ):

        conn = get_connection()

        if conn:

            cursor = conn.cursor()

            hashed = bcrypt.hashpw(
                password.encode(),
                bcrypt.gensalt()
            )

            try:

                cursor.execute(
                    """
                    INSERT INTO users
                    (username,email,password,role)
                    VALUES(%s,%s,%s,%s)
                    """,
                    (
                        username,
                        email,
                        hashed.decode(),
                        role
                    )
                )

                conn.commit()

                st.success(
                    "Account Created Successfully"
                )

            except Exception as e:

                st.error(e)

            finally:

                cursor.close()
                conn.close()

# ============================================
# LOGIN
# ============================================

def login_page():

    st.header("🔐 Login")

    username = st.text_input(
        "Username",
        key="login_user"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_pass"
    )

    if st.button(
        "Login",
        key="login_btn"
    ):

        conn = get_connection()

        if conn:

            cursor = conn.cursor(
                dictionary=True
            )

            cursor.execute(
                """
                SELECT *
                FROM users
                WHERE username=%s
                """,
                (username,)
            )

            user = cursor.fetchone()

            if user:

                if bcrypt.checkpw(
                    password.encode(),
                    user["password"].encode()
                ):

                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.role = user["role"]

                    st.success(
                        "Login Successful"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid Password"
                    )

            else:

                st.error(
                    "User Not Found"
                )

            cursor.close()
            conn.close()

# ============================================
# FORGOT PASSWORD
# ============================================

def forgot_password_page():

    st.header("🔑 Forgot Password")

    username = st.text_input(
        "Username",
        key="forgot_user"
    )

    if st.button(
        "Generate OTP",
        key="forgot_btn"
    ):

        st.session_state.otp = generate_otp()

        st.success(
            f"OTP: {st.session_state.otp}"
        )

# ============================================
# RESET PASSWORD
# ============================================

def reset_password_page():

    st.header("🔄 Reset Password")

    username = st.text_input(
        "Username",
        key="reset_user"
    )

    otp = st.text_input(
        "OTP",
        key="reset_otp"
    )

    new_password = st.text_input(
        "New Password",
        type="password",
        key="reset_pass"
    )

    if st.button(
        "Reset Password",
        key="reset_btn"
    ):

        if otp == st.session_state.otp:

            conn = get_connection()

            cursor = conn.cursor()

            hashed = bcrypt.hashpw(
                new_password.encode(),
                bcrypt.gensalt()
            )

            cursor.execute(
                """
                UPDATE users
                SET password=%s
                WHERE username=%s
                """,
                (
                    hashed.decode(),
                    username
                )
            )

            conn.commit()

            st.success(
                "Password Reset Successful"
            )

            cursor.close()
            conn.close()

        else:

            st.error(
                "Invalid OTP"
            )

# ============================================
# LOGOUT
# ============================================

def logout():

    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

    st.rerun()
    # ============================================
# MUSIC PERSONALITY ANALYZER
# ============================================

spotify_links = {
    "Rock":
    "https://open.spotify.com/playlist/37i9dQZF1DWXRqgorJj26U",

    "Pop":
    "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M",

    "EDM":
    "https://open.spotify.com/playlist/37i9dQZF1DX4dyzvuaRJ0n",

    "Lo-Fi":
    "https://open.spotify.com/playlist/0vvXsWCC9xrXsKd4FyS8kM",

    "Classical":
    "https://open.spotify.com/playlist/37i9dQZF1DWWEJlAGA9gs0"
}

# ============================================
# SAVE RESULT
# ============================================

def save_result(
    username,
    personality,
    genre,
    score
):

    conn = get_connection()

    if conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO results
            (
                username,
                personality,
                genre,
                score
            )
            VALUES(%s,%s,%s,%s)
            """,
            (
                username,
                personality,
                genre,
                score
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

# ============================================
# PERSONALITY DESCRIPTIONS
# ============================================

def personality_description(personality):

    descriptions = {

        "Calm Thinker":
        """
        You enjoy peaceful environments,
        emotional balance and deep focus.
        """,

        "Party Lover":
        """
        You love excitement,
        social activities and fun experiences.
        """,

        "Energetic Explorer":
        """
        You enjoy adventure,
        challenges and motivation.
        """,

        "Deep Analyst":
        """
        You are logical,
        intelligent and thoughtful.
        """,

        "Creative Soul":
        """
        You are imaginative,
        artistic and expressive.
        """
    }

    return descriptions.get(
        personality,
        "No description available."
    )

# ============================================
# ANALYZER PAGE
# ============================================

def analyzer_page():

    st.title("🎧 Music Personality Analyzer")

    st.markdown("""
    ### Answer these questions
    and discover your music personality.
    """)

    q1 = st.radio(
        "1. What do you do when stressed?",
        [
            "Listen to calm music",
            "Go to a party",
            "Exercise",
            "Read books"
        ]
    )

    q2 = st.radio(
        "2. Your ideal weekend?",
        [
            "Relax at home",
            "Concert",
            "Adventure trip",
            "Study"
        ]
    )

    q3 = st.radio(
        "3. Favorite music style?",
        [
            "Soft",
            "Dance",
            "Guitar",
            "Instrumental"
        ]
    )

    q4 = st.radio(
        "4. Your energy level?",
        [
            "Very High",
            "Medium",
            "Low"
        ]
    )

    q5 = st.radio(
        "5. When do you listen to music?",
        [
            "Studying",
            "Travelling",
            "Parties",
            "Sleeping"
        ]
    )

    if st.button(
        "🔍 Analyze Personality"
    ):

        personality = ""
        genre = ""
        score = 0

        # =====================
        # RULE BASED ANALYSIS
        # =====================

        if (
            q1 == "Listen to calm music"
            and q2 == "Relax at home"
        ):

            personality = "Calm Thinker"
            genre = "Lo-Fi"
            score = 95

        elif (
            q2 == "Concert"
            or q3 == "Dance"
        ):

            personality = "Party Lover"
            genre = "EDM"
            score = 92

        elif (
            q3 == "Guitar"
            or q4 == "Very High"
        ):

            personality = "Energetic Explorer"
            genre = "Rock"
            score = 89

        elif (
            q3 == "Instrumental"
            or q2 == "Study"
        ):

            personality = "Deep Analyst"
            genre = "Classical"
            score = 93

        else:

            personality = "Creative Soul"
            genre = "Pop"
            score = 87

        # =====================
        # SAVE TO MYSQL
        # =====================

        save_result(
            st.session_state.username,
            personality,
            genre,
            score
        )

        # =====================
        # RESULT CARD
        # =====================

        st.success(
            "Analysis Completed Successfully"
        )

        st.markdown("---")

        st.subheader(
            "🎯 Your Personality"
        )

        st.info(personality)

        st.subheader(
            "📖 Description"
        )

        st.write(
            personality_description(
                personality
            )
        )

        st.subheader(
            "🎵 Recommended Genre"
        )

        st.success(genre)

        st.subheader(
            "📈 Compatibility Score"
        )

        st.progress(
            score / 100
        )

        st.write(
            f"### {score}% Match"
        )

        st.subheader(
            "🎧 Spotify Playlist"
        )

        st.link_button(
            "Open Spotify Playlist",
            spotify_links[genre]
        )

        st.balloons()

# ============================================
# USER HISTORY
# ============================================

def get_user_history(username):

    conn = get_connection()

    if conn:

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT *
            FROM results
            WHERE username=%s
            ORDER BY id DESC
            """,
            (username,)
        )

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return data

    return []

# ============================================
# TOTAL ANALYSIS COUNT
# ============================================

def get_total_analysis():

    conn = get_connection()

    if conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM results
            """
        )

        total = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return total

    return 0
# ============================================
# DASHBOARD MODULE
# ============================================

import pandas as pd
import matplotlib.pyplot as plt

# ============================================
# TOTAL USERS
# ============================================

def get_total_users():

    conn = get_connection()

    if conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM users
            """
        )

        total = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return total

    return 0

# ============================================
# MOST POPULAR PERSONALITY
# ============================================

def get_popular_personality():

    conn = get_connection()

    if conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT personality,
            COUNT(*) as total
            FROM results
            GROUP BY personality
            ORDER BY total DESC
            LIMIT 1
            """
        )

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return row[0]

    return "No Data"

# ============================================
# STUDENT DASHBOARD
# ============================================

def student_dashboard():

    st.title("📊 Student Dashboard")

    username = st.session_state.username

    history = get_user_history(username)

    if len(history) == 0:

        st.warning(
            "No Analysis History Found"
        )

        return

    df = pd.DataFrame(history)

    # =========================
    # METRICS
    # =========================

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Analyses",
        len(df)
    )

    col2.metric(
        "Average Score",
        int(df["score"].mean())
    )

    col3.metric(
        "Top Personality",
        df["personality"].mode()[0]
    )

    st.markdown("---")

    st.subheader(
        "📜 Analysis History"
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    # =========================
    # SCORE TREND
    # =========================

    st.subheader(
        "📈 Score Trend"
    )

    st.line_chart(
        df["score"]
    )

    # =========================
    # PIE CHART
    # =========================

    st.subheader(
        "🎯 Personality Distribution"
    )

    personality_count = (
        df["personality"]
        .value_counts()
    )

    fig, ax = plt.subplots()

    ax.pie(
        personality_count,
        labels=personality_count.index,
        autopct="%1.1f%%"
    )

    st.pyplot(fig)

# ============================================
# FETCH ALL USERS
# ============================================

def fetch_users():

    conn = get_connection()

    if conn:

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT *
            FROM users
            """
        )

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return data

    return []

# ============================================
# FETCH ALL RESULTS
# ============================================

def fetch_results():

    conn = get_connection()

    if conn:

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT *
            FROM results
            """
        )

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return data

    return []

# ============================================
# SEARCH USER
# ============================================

def search_user():

    st.subheader(
        "🔍 Search User Records"
    )

    username = st.text_input(
        "Enter Username",
        key="search_user"
    )

    if st.button(
        "Search"
    ):

        conn = get_connection()

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT *
            FROM results
            WHERE username=%s
            """,
            (username,)
        )

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        if len(data) == 0:

            st.error(
                "No Records Found"
            )

        else:

            st.dataframe(
                pd.DataFrame(data),
                use_container_width=True
            )

# ============================================
# ADMIN DASHBOARD
# ============================================

def admin_dashboard():

    st.title(
        "🛠 Admin Dashboard"
    )

    total_users = get_total_users()

    total_analysis = get_total_analysis()

    popular = get_popular_personality()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "👥 Total Users",
        total_users
    )

    col2.metric(
        "🎵 Total Analyses",
        total_analysis
    )

    col3.metric(
        "🏆 Popular Personality",
        popular
    )

    st.markdown("---")

    # =========================
    # USERS TABLE
    # =========================

    st.subheader(
        "👤 Registered Users"
    )

    users_df = pd.DataFrame(
        fetch_users()
    )

    st.dataframe(
        users_df,
        use_container_width=True
    )

    st.markdown("---")

    # =========================
    # RESULTS TABLE
    # =========================

    st.subheader(
        "📊 Analysis Records"
    )

    results_df = pd.DataFrame(
        fetch_results()
    )

    st.dataframe(
        results_df,
        use_container_width=True
    )

    # =========================
    # PERSONALITY CHART
    # =========================

    if len(results_df) > 0:

        st.subheader(
            "🎯 Personality Popularity"
        )

        personality_chart = (
            results_df["personality"]
            .value_counts()
        )

        st.bar_chart(
            personality_chart
        )

        # =====================
        # PIE CHART
        # =====================

        st.subheader(
            "🥧 Personality Distribution"
        )

        fig, ax = plt.subplots()

        ax.pie(
            personality_chart,
            labels=personality_chart.index,
            autopct="%1.1f%%"
        )

        st.pyplot(fig)

        # =====================
        # GENRE POPULARITY
        # =====================

        st.subheader(
            "🎧 Genre Popularity"
        )

        genre_chart = (
            results_df["genre"]
            .value_counts()
        )

        st.bar_chart(
            genre_chart
        )

# ============================================
# ADMIN ANALYTICS SUMMARY
# ============================================

def analytics_summary():

    st.subheader(
        "📈 System Analytics"
    )

    users = get_total_users()

    analyses = get_total_analysis()

    st.write(
        f"Total Registered Users : {users}"
    )

    st.write(
        f"Total Analyses Done : {analyses}"
    )

    if analyses > 0:

        st.success(
            "System Running Successfully"
        )
        # ============================================
# PDF REPORT MODULE
# ============================================

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

# ============================================
# GENERATE PDF
# ============================================

def generate_pdf(username):

    filename = f"{username}_report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "MusicMind AI Personality Report",
        styles["Title"]
    )

    elements.append(title)
    elements.append(Spacer(1,20))

    elements.append(
        Paragraph(
            f"<b>User:</b> {username}",
            styles["Normal"]
        )
    )

    elements.append(
        Spacer(1,20)
    )

    history = get_user_history(
        username
    )

    if len(history) == 0:

        elements.append(
            Paragraph(
                "No Analysis Records Found",
                styles["Normal"]
            )
        )

    else:

        for row in history:

            elements.append(
                Paragraph(
                    f"<b>Personality:</b> {row['personality']}",
                    styles["Normal"]
                )
            )

            elements.append(
                Paragraph(
                    f"<b>Genre:</b> {row['genre']}",
                    styles["Normal"]
                )
            )

            elements.append(
                Paragraph(
                    f"<b>Score:</b> {row['score']}%",
                    styles["Normal"]
                )
            )

            elements.append(
                Paragraph(
                    f"<b>Date:</b> {row['created_at']}",
                    styles["Normal"]
                )
            )

            elements.append(
                Spacer(1,10)
            )

    doc.build(elements)

    return filename

# ============================================
# HOME PAGE
# ============================================

def home_page():

    st.markdown("""
    <div style='text-align:center;'>

    <h1 style='font-size:60px;'>
    🎧 MusicMind AI
    </h1>

    <h3>
    Discover Your Personality Through Music
    </h3>

    </div>
    """,
    unsafe_allow_html=True)

# ============================================
# LOGIN AREA
# ============================================

if not st.session_state.logged_in:

    home_page()

    page = st.radio(
        "",
        [
            "🔐 Login",
            "📝 Signup",
            "🔑 Forgot Password",
            "🔄 Reset Password"
        ],
        horizontal=True
    )

    if page == "🔐 Login":
        login_page()

    elif page == "📝 Signup":
        signup_page()

    elif page == "🔑 Forgot Password":
        forgot_password_page()

    elif page == "🔄 Reset Password":
        reset_password_page()

# ============================================
# STUDENT PANEL
# ============================================

elif st.session_state.role == "student":

    st.title(
        f"🎵 Welcome {st.session_state.username}"
    )

    tab1, tab2, tab3 = st.tabs([
        "🎧 Analyzer",
        "📊 Dashboard",
        "📄 Reports"
    ])

    with tab1:

        analyzer_page()

    with tab2:

        student_dashboard()

    with tab3:

        st.subheader(
            "Generate Personality Report"
        )

        if st.button(
            "Generate PDF Report"
        ):

            pdf = generate_pdf(
                st.session_state.username
            )

            with open(
                pdf,
                "rb"
            ) as f:

                st.download_button(
                    label="📄 Download PDF",
                    data=f,
                    file_name=pdf,
                    mime="application/pdf"
                )

    st.button(
        "🚪 Logout",
        on_click=logout
    )

# ============================================
# ADMIN PANEL
# ============================================

elif st.session_state.role == "admin":

    st.title(
        "🛠 MusicMind AI Admin Panel"
    )

    tab1, tab2, tab3 = st.tabs([
        "📊 Dashboard",
        "🔍 Search User",
        "📈 Analytics"
    ])

    with tab1:

        admin_dashboard()

    with tab2:

        search_user()

    with tab3:

        analytics_summary()

    st.button(
        "🚪 Logout",
        on_click=logout
    )