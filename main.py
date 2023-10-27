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
    def __init__(self, root_path):
        self.images = []
        for root, _, files in os.walk(root_path):
            for file in files:
                if file.lower().endswith(('png', 'jpg', 'jpeg', 'png', 'heic', 'heic', 'mov')):
                    self.images.append(os.path.join(root, file))
        self.current_index = 0

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

    if st.button('Select Root Path'):
        root_path = select_directory(title="Select Root Folder")
        st.session_state.root_path = root_path  # Save the selected path in session state

    if st.button('Select Destination Path'):
        dest_path = select_directory(title="Select Destination Folder")
        st.session_state.dest_path = dest_path  # Save the selected path in session state

    # Check if both paths are available in session state
    if 'root_path' in st.session_state and 'dest_path' in st.session_state:
        root_path = st.session_state.root_path
        dest_path = st.session_state.dest_path
        st.write(f"Root Path: {root_path}")
        st.write(f"Destination Path: {dest_path}")

        if 'img_browser' not in st.session_state:
            st.session_state.img_browser = ImageBrowser(root_path)

        img_browser = st.session_state.img_browser

        prev_img_path = img_browser.get_image(-1)
        curr_img_path = img_browser.get_image()
        next_img_path = img_browser.get_image(1)

        button_col1, button_col2, button_col3, button_col4 = st.columns([.20, .20, .20, .20])
        with button_col1:
            liked = st.button("👍", key="like", help="Copy to destination folder")
        with button_col2:
            disliked = st.button("👎", key="dislike", help="Skip")
        with button_col3:
            prev = st.button("⬅️", key="prev")
        with button_col4:
            nxt = st.button("➡️", key="next")

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

        if liked:
            img_browser.copy_to_dest(dest_path, root_path)
            img_browser.next()
        elif disliked:
            img_browser.next()
        elif prev:
            img_browser.prev()
        elif nxt:
            img_browser.next()


if __name__ == "__main__":
    main()
