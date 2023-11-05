# Pic Selector
![example workflow](https://github.com/tsadoq/pic-selector/actions/workflows/python-app.yml/badge.svg)

## Overview
This Pic Selector is a Streamlit-based application designed to streamline the process of sorting through a large collection of images. Users can quickly browse through images, choose which ones to keep, and seamlessly copy selected images to a specified destination while maintaining the original folder structure.

## Features
- **Browse Images**: Navigate through images using a simple and intuitive interface similar to a dating app.
- **Folder Selection**: Use a GUI-based folder picker to select both the source and destination folders without needing to type any paths.
- **Selective Copying**: Choose images you like and copy them to the destination folder with a single click.
- **Folder Structure Preservation**: Maintain the same folder hierarchy in the destination as found in the source.

## Installation

To get started with the Pic Selector, follow these steps:

1. Ensure you have Python installed on your system. This app is compatible with Python 3.6 and above.

2. Clone the repository:

    ```bash
    git clone
    ```

3. Navigate to the app directory:
    ```bash
   cd pic-selector
    ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Run the app:
    ```bash
    streamlit run picture_selector.py
    ```

## Usage

1. Launch the application and click the buttons to select the source and destination directories.

2. Use the provided buttons to navigate through your images:
- Click **Like** to copy the current image to the destination folder.
- Click **Dislike** to skip the image.
- Use **Previous** and **Next** to navigate backward and forward in the image list.

3. View the selected and deselected images within their corresponding directories.

## Contributing
Contributions to the Pic Selector are welcome! If you have a suggestion that would make this app better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Acknowledgements
- [Streamlit](https://streamlit.io/)
- [Python Imaging Library (PIL)](https://python-pillow.org/)
- [tkinter](https://docs.python.org/3/library/tkinter.html)
- [pillow_heif](https://pypi.org/project/pillow-heif/)

