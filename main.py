import streamlit as st
import os
import shutil
import tkinter as tk
from tkinter import filedialog
import multiprocessing

from pillow_heif import register_heif_opener

register_heif_opener()

st.set_page_config(layout="wide")


class ImageBrowser:
    def __init__(self, root_path, dest_path):
        self.dest_images = None
        self.images = None

        self.tot_dest_images = 0
        self.tot_root_images = 0

        self.load_source_images(root_path)
        self.load_selected_images(dest_path)
        if self.dest_images:
            print(f"Found {len(self.dest_images)} images in {dest_path}")
            self.current_index = self.images.index(self.dest_images[-1].replace(dest_path, root_path))
        else:
            self.current_index = 0

    def load_source_images(self, root_path):
        self.images = []
        for root, _, files in os.walk(root_path):
            for file in files:
                if file.lower().endswith(('png', 'jpg', 'jpeg', 'png', 'heif', 'heic', 'mov')):
                    self.images.append(os.path.join(root, file))
        self.images.sort()
        self.tot_root_images = len(self.images)


    def load_selected_images(self, dest_path):
        self.dest_images = []
        for root, _, files in os.walk(dest_path):
            for file in files:
                if file.lower().endswith(('png', 'jpg', 'jpeg', 'png', 'heif', 'heic', 'mov')):
                    self.dest_images.append(os.path.join(root, file))
        self.dest_images.sort()
        self.tot_dest_images = len(self.dest_images)


    def get_image(self, offset=0):
        return self.images[self.current_index + offset] if 0 <= self.current_index + offset < len(self.images) else None

    def next(self):
        if self.current_index + 1 < len(self.images):
            self.current_index += 1

    def prev(self):
        if self.current_index - 1 >= 0:
            self.current_index -= 1

    def copy_to_dest(self, dest_path, root_path):
        src = self.images[self.current_index]
        dest = os.path.join(dest_path, os.path.relpath(src, root_path))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(src, dest)
        self.load_selected_images(dest_path)


def on_like():
    if 'img_browser' in st.session_state:
        st.session_state.img_browser.copy_to_dest(st.session_state.dest_path, st.session_state.root_path)
        st.session_state.img_browser.next()


def on_dislike():
    if 'img_browser' in st.session_state:
        st.session_state.img_browser.next()


def on_prev():
    if 'img_browser' in st.session_state:
        st.session_state.img_browser.prev()


def on_next():
    if 'img_browser' in st.session_state:
        st.session_state.img_browser.next()


def select_directory(title="Select Folder"):
    # Create a queue to share data between processes
    queue = multiprocessing.Queue()

    # Start a new process to show the directory picker
    process = multiprocessing.Process(target=show_directory_picker, args=(queue, title))
    process.start()

    # Wait for the process to finish and get the selected directory
    directory = queue.get()
    process.join()
    return directory


def show_directory_picker(queue, title):
    root = tk.Tk()
    root.withdraw()  # Hides the small tkinter window.
    directory = filedialog.askdirectory(title=title)  # Shows the directory picker dialog
    queue.put(directory)  # Put the selected directory in the queue


def main():
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
                st.image(next_img_path, use_column_width=True)


if __name__ == "__main__":
    main()
