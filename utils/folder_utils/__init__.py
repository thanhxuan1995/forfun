import os


def create_directory(directory: str) -> None:
    # Function to check and create a directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
