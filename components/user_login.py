import streamlit as st
from utils.db import db, initialize_session_from_db
from utils.i18n import tr

def show_user_login():
    """Display a login/registration form for name & shop name-based user identification."""
    lang = st.selectbox(
        tr("choose_language"),
        ["English", "Bahasa Indonesia"],
        index=["English", "Bahasa Indonesia"].index(st.session_state.get("language", "English")),
        key="login_language"
    )
    if st.session_state.get("language") != lang:
        st.session_state["language"] = lang

    st.markdown(f"## {tr('welcome')}")
    st.markdown(tr('please_enter'))

    with st.form(key="user_login_form"):
        name = st.text_input(tr("your_name"), value=st.session_state.get("player_name", ""))
        shop_name = st.text_input(tr("shop_name"), value=st.session_state.get("shop_name", ""))
        submit = st.form_submit_button(tr("continue"))

    if submit:
        if not name.strip() or not shop_name.strip():
            st.warning(tr("please_enter_both"))
            st.stop()

        # Try to find user in DB by name and shop name
        user = db.get_user_by_name_and_shop(name.strip(), shop_name.strip())
        if user:
            # Existing user: initialize session from DB
            initialize_session_from_db(user["user_id"])
            st.session_state.user_id = user["user_id"]
            st.session_state.player_name = user["name"]
            st.session_state.shop_name = user.get("shop_name", shop_name.strip())
            st.success(tr("success_welcome_back", player_name=name, shop_name=shop_name))
            st.rerun()
        else:
            # New user: create and initialize
            user_id = db.create_user(name.strip(), {"shop_name": shop_name.strip()})
            initialize_session_from_db(user_id)
            st.session_state.user_id = user_id
            st.session_state.player_name = name.strip()
            st.session_state.shop_name = shop_name.strip()
            st.success(tr("success_welcome", player_name=name))
            st.rerun()

# ---
# You will need to add the following method to your DatabaseManager class in utils/db.py:
#
# def get_user_by_name_and_shop(self, name, shop_name):
#     conn = self.get_connection()
#     cursor = conn.cursor()
#     try:
#         cursor.execute(
#             "SELECT * FROM users WHERE name = ? AND (metadata LIKE ? OR metadata LIKE ?)",
#             (name, f'%\"shop_name\": \"{shop_name}\"%', f'%\"shop_name\": \"{shop_name}\"%')
#         )
#         row = cursor.fetchone()
#         return dict(row) if row else None
#     finally:
#         self.close_connection()
