import multiprocessing
import tkinter as tk
from tkinter import filedialog
from typing import Optional


def select_directory(
    title: Optional[str] = "Select Folder",
) -> str:
    """
    Show a directory picker dialog and return the selected directory.
    :param title: title of the directory picker dialog
    :return: selected directory
    """
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=show_directory_picker, args=(queue, title))
    process.start()
    directory = queue.get()
    process.join()
    return directory


def show_directory_picker(
    queue: multiprocessing.Queue,
    title: str,
):
    """
    Show a directory picker dialog and put the selected directory in the queue.
    :param queue: queue of file paths
    :param title: title of the directory picker dialog
    :return: None
    """
    root = tk.Tk()
    root.withdraw()  # Hides the small tkinter window.
    directory = filedialog.askdirectory(title=title)  # Shows the directory picker dialog
    queue.put(directory)  # Put the selected directory in the queue
