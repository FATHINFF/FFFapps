import streamlit as st

def login():
    # Gunakan st.markdown untuk mengatur tata letak ke tengah
    st.markdown(
        """
        <div style='display: flex; justify-content: center; align-items: center; height: 10vh;'>
            <div>
                <h1>Login </h1>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Form login di bawah heading
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":  # Ganti dengan validasi yang lebih aman
            st.success("Login successful")
            st.session_state.logged_in = True  # Set session state ke logged_in setelah login berhasil
            st.rerun()  # Gunakan st.rerun() untuk me-refresh halaman
        else:
            st.error("Invalid username or password")
            return False

    return False

import streamlit as st

def login():
    # Gunakan st.markdown untuk mengatur tata letak ke tengah
    st.markdown(
        """
        <div style='display: flex; justify-content: center; align-items: center; height: 10vh;'>
            <div>
                <h1>Login </h1>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Form login di bawah heading
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":  # Ganti dengan validasi yang lebih aman
            st.success("Login successful")
            st.session_state.logged_in = True  # Set session state ke logged_in setelah login berhasil
            st.rerun()  # Gunakan st.rerun() untuk me-refresh halaman
        else:
            st.error("Invalid username or password")
            return False

    return False
