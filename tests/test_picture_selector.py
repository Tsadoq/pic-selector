import os.path

from streamlit.testing.v1 import AppTest


def test_picture_selector():
    at = AppTest.from_file("../picture_selector.py")
    assert not at.exception


def test_picture_selector_read_files():
    at = AppTest.from_file("../picture_selector.py")
    at.session_state.root_path = os.path.abspath('./resources/root_test')
    at.session_state.dest_path = os.path.abspath('./resources/dest_test')
    at.columns[1].button(key='next')
    at.button(key='like')
    at.button(key='next')
    at.button(key='like')

    assert at.session_state.img_browser.tot_root_images == 2
