import streamlit as st


def on_like():
    """
    Copy the current image to the destination folder and move to the next image
    """
    if 'img_browser' in st.session_state:
        st.session_state.img_browser.copy_to_dest(st.session_state.dest_path, st.session_state.root_path)
        st.session_state.img_browser.next()


def on_dislike():
    """
    Skip the current image and move to the next image
    """
    if 'img_browser' in st.session_state:
        st.session_state.img_browser.next()


def on_prev():
    """
    Move to the previous image
    """
    if 'img_browser' in st.session_state:
        st.session_state.img_browser.prev()


def on_next():
    """
    Move to the next image
    """
    if 'img_browser' in st.session_state:
        st.session_state.img_browser.next()
