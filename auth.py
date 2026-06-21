import streamlit as st
import bcrypt
import random

from db import (
    execute_query,
    fetch_query,
    get_user,
    user_exists,
    save_otp,
    verify_otp
)

# ==========================
# PASSWORD FUNCTIONS
# ==========================

def hash_password(password):
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(
        password.encode(),
        hashed.encode()
    )

# ==========================
# SIGNUP
# ==========================

def signup_page():

    st.subheader("📝 Student Signup")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input(
        "Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button("Create Account"):

        if not username or not email or not password:
            st.error("All fields required")
            return

        if password != confirm_password:
            st.error("Passwords do not match")
            return

        if user_exists(username, email):
            st.error("User already exists")
            return

        hashed = hash_password(password)

        query = """
        INSERT INTO users
        (username,email,password)
        VALUES(%s,%s,%s)
        """

        success = execute_query(
            query,
            (
                username,
                email,
                hashed
            )
        )

        if success:
            st.success(
                "Account Created Successfully"
            )

# ==========================
# LOGIN
# ==========================

def login_page():

    st.subheader("🔐 Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        user = get_user(username)

        if user is None:
            st.error("User not found")
            return

        if check_password(
            password,
            user["password"]
        ):

            st.session_state.logged_in = True
            st.session_state.username = user["username"]
            st.session_state.role = user["role"]

            st.success("Login Successful")

            st.rerun()

        else:
            st.error("Invalid Password")

# ==========================
# LOGOUT
# ==========================

def logout():

    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

    st.rerun()

# ==========================
# FORGOT PASSWORD
# ==========================

def forgot_password_page():

    st.subheader("🔑 Forgot Password")

    username = st.text_input(
        "Username"
    )

    if st.button("Generate OTP"):

        user = get_user(username)

        if user is None:
            st.error("User not found")
            return

        otp = str(
            random.randint(
                100000,
                999999
            )
        )

        save_otp(
            username,
            otp
        )

        st.success(
            f"Demo OTP : {otp}"
        )

# ==========================
# RESET PASSWORD
# ==========================

def reset_password_page():

    st.subheader("🔄 Reset Password")

    username = st.text_input(
        "Username"
    )

    otp = st.text_input(
        "OTP"
    )

    new_password = st.text_input(
        "New Password",
        type="password"
    )

    if st.button("Reset Password"):

        if not verify_otp(
            username,
            otp
        ):
            st.error("Invalid OTP")
            return

        hashed = hash_password(
            new_password
        )

        query = """
        UPDATE users
        SET password=%s
        WHERE username=%s
        """

        execute_query(
            query,
            (
                hashed,
                username
            )
        )

        st.success(
            "Password Updated Successfully"
        )

# ==========================
# SESSION INIT
# ==========================

def initialize_session():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "username" not in st.session_state:
        st.session_state.username = ""

    if "role" not in st.session_state:
        st.session_state.role = ""