import streamlit as st

from pillow_heif import register_heif_opener

from utils.callbacks import on_like, on_dislike, on_prev, on_next
from utils.file_interface import select_directory
from utils.image_browser import ImageBrowser

register_heif_opener()

st.set_page_config(layout="wide")


def select_pictures():
    st.title("Image Selector")
    if 'img_browser' in st.session_state:
        cursor_col, percentage_col = st.columns(2)
        with cursor_col:
            st.progress(
                value=st.session_state.img_browser.current_index / st.session_state.img_browser.tot_root_images,
                text=f'Viewing {st.session_state.img_browser.current_index} out of {st.session_state.img_browser.tot_root_images} images'
            )
        with percentage_col:
            st.progress(
                value=st.session_state.img_browser.tot_dest_images / st.session_state.img_browser.tot_root_images,
                text=f'Copied {st.session_state.img_browser.tot_dest_images} out of {st.session_state.img_browser.tot_root_images} images'
            )

    col_root, col_dest = st.columns(2)
    with col_root:
        if st.button('Select Root Path'):
            root_path = select_directory(title="Select Root Folder")
            st.session_state.root_path = root_path  # Save the selected path in session state
            st.write(f"Root Path: {st.session_state.root_path}")

    with col_dest:
        if st.button('Select Destination Path'):
            dest_path = select_directory(title="Select Destination Folder")
            st.session_state.dest_path = dest_path  # Save the selected path in session state
            st.write(f"Destination Path: {st.session_state.dest_path}")

    # Check if both paths are available in session state
    if 'root_path' in st.session_state and 'dest_path' in st.session_state:
        if 'img_browser' not in st.session_state:
            st.session_state.img_browser = ImageBrowser(
                root_path=st.session_state.root_path,
                dest_path=st.session_state.dest_path,
            )

        prev_img_path = st.session_state.img_browser.get_image(-1)
        curr_img_path = st.session_state.img_browser.get_image()
        next_img_path = st.session_state.img_browser.get_image(1)

        _, button_col1, button_col2, button_col3, button_col4, _ = st.columns([.30, .10, .10, .10, .10, .30])
        with button_col1:
            st.button("👍", key="like", help="Copy to destination folder", on_click=on_like)
        with button_col2:
            st.button("👎", key="dislike", help="Skip", on_click=on_dislike)
        with button_col3:
            st.button("⬅️", key="prev", help="Previous", on_click=on_prev)
        with button_col4:
            st.button("➡️", key="next", help="Next", on_click=on_next)

        col1, col2, col3 = st.columns([.20, .6, .20])
        if prev_img_path:
            with col1:
                st.image(prev_img_path, use_column_width=True)
        with col2:
            if curr_img_path:
                st.image(curr_img_path, use_column_width=True)
        if next_img_path:
            with col3:
                print(next_img_path)
                st.image(next_img_path, use_column_width=True)


if __name__ == "__main__":
    select_pictures()
