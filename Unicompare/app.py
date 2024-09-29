import streamlit as st
from unicompare import unicompare
from home import home
from superset import create_superset
from addcourse import add_course
import pandas as pd

USER_CREDENTIALS = {
    "admin": "password123",
    "user1": "user1password",
    "j": "j"
}

st.set_page_config(page_title="Unicompare", layout="wide")

def is_authenticated():
    return 'authenticated' in st.session_state and st.session_state.authenticated

def authenticate(username, password):
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        st.session_state.authenticated = True
        return True
    else:
        st.error("Invalid username or password")
        return False

data = pd.read_csv('data/Final dataset.csv')
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

if 'page' not in st.session_state:
    st.session_state.page = "Home"
if 'page_number' not in st.session_state:
    st.session_state.page_number = 0
if 'superset_data' not in st.session_state:
    st.session_state.superset_data = None

st.markdown("""
    <style>
    body {
        background-size: cover;
    }
    .login-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 30px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
        text-align: center;
    }
    input {
        border: none;
        border-bottom: 2px solid #3498db;
        font-size: 16px;
        padding: 10px;
        width: 100%;
        margin: 0;
    }
    div.css-1r5t16f {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    input:focus {
        border-color: #2980b9;
        outline: none;
    }
    /* Specific style for login and logout buttons */
    .login-logout-button > button:first-child {
        background-color: #3498db;
        color: white;
        border-radius:10px;
        height:3em;
        width:auto;
        padding: 0 2em;
        font-size:16px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    .login-logout-button > button:hover {
        background-color: #2980b9;
        color: white;
    }
    .title {
        text-align: center;
        color: #3498db;
        font-family: 'Arial', sans-serif;
    }
    .logout-button {
        position: fixed;
        top: 20px;
        left: 20px;
        background-color: #e74c3c;
        color: white;
        padding: 8px 16px;
        font-size: 12px;
        border-radius: 5px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
        width: auto;
    }
    .logout-button:hover {
        background-color: #c0392b;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

if not is_authenticated():
    st.markdown("<h1 class='title'>Welcome to Unicompare</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='title' style='color: #2c3e50;'>Please login to continue</h3>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form(key='login_form'):
            username = st.text_input("👤 Username")
            password = st.text_input("🔒 Password", type="password")
            st.markdown('</div>', unsafe_allow_html=True)

            login_button = st.form_submit_button("Login")

            if login_button:
                if authenticate(username, password):
                    st.experimental_rerun()

if is_authenticated():
    if st.session_state.page == "Home":
        home()
        
        logout_button = st.button("Logout", key="logout")
        if logout_button:
            st.session_state.authenticated = False
            st.experimental_rerun()

    elif st.session_state.page == "Unicompare":
        unicompare(data)
    elif st.session_state.page == "Superset":
        st.title("Superset")
        if st.session_state.superset_data is not None:
            create_superset(st.session_state.superset_data)
    elif st.session_state.page == "Add Course":
        add_course(data)
