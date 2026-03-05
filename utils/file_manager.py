import os
from config import PROJECT_FOLDER_NAME


def get_project_path() -> str:
    """Returns the full path to the project folder on the Desktop."""
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    return os.path.join(desktop_path, PROJECT_FOLDER_NAME)


def create_project_folder() -> str:
    """
    Creates the project output folder on the Desktop if it doesn't exist.
    Returns the full path to the folder.
    """
    project_path = get_project_path()

    if not os.path.exists(project_path):
        os.makedirs(project_path)

    return project_path
