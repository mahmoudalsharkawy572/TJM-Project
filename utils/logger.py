import logging
import os


def setup_logger(project_path: str) -> None:
    """
    Initializes the file logger.
    Must be called AFTER create_project_folder() so the path exists.
    """
    log_path = os.path.join(project_path, "automation.log")

    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    logging.info("Logger initialized.")
