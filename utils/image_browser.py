import os
import shutil
from typing import Optional


class ImageBrowser:
    """
    Class used to browse images in a folder and copy them to a destination folder.
    """
    def __init__(
        self,
        root_path: str,
        dest_path: str,
    ):
        """
        Set the root path and the destination path and load the images in the root path and the selected images in
        the destination path.
        :param root_path: path to the root folder
        :param dest_path: path to the destination folder
        """
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

    def load_source_images(
        self,
        root_path: str,
    ) -> None:
        """
        Load the images in the root path.
        :param root_path: path to the root folder
        :return: None
        """
        self.images = []
        for root, _, files in os.walk(root_path):
            for file in files:
                if file.lower().endswith(('png', 'jpg', 'jpeg', 'png', 'heif', 'heic', 'mov')):
                    self.images.append(os.path.join(root, file))
        self.images.sort()
        self.tot_root_images = len(self.images)


    def load_selected_images(
        self,
        dest_path: str,
    ) -> None:
        """
        Load the images in the destination path.
        :param dest_path: path to the destination folder
        :return: None
        """
        self.dest_images = []
        for root, _, files in os.walk(dest_path):
            for file in files:
                if file.lower().endswith(('png', 'jpg', 'jpeg', 'png', 'heif', 'heic', 'mov')):
                    self.dest_images.append(os.path.join(root, file))
        self.dest_images.sort()
        self.tot_dest_images = len(self.dest_images)


    def get_image(
        self,
        offset: Optional[int]=0,
    ) -> Optional[str]:
        """
        Get the image at the current index + offset.
        :param offset: offset from the current index
        :return: path to the image
        """
        return self.images[self.current_index + offset] if 0 <= self.current_index + offset < len(self.images) else None

    def next(self):
        """
        Increment the current index if possible.
        """
        if self.current_index + 1 < len(self.images):
            self.current_index += 1

    def prev(self):
        """
        Decrement the current index if possible.
        """
        if self.current_index - 1 >= 0:
            self.current_index -= 1

    def copy_to_dest(
        self,
        dest_path: str,
        root_path: str,
    ) -> None:
        """
        Copy the current image to the destination path.
        :param dest_path: path to the destination folder
        :param root_path: path to the root folder
        :return: None
        """
        src = self.images[self.current_index]
        dest = os.path.join(dest_path, os.path.relpath(src, root_path))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(src, dest)
        self.load_selected_images(dest_path)
