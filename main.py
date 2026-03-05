import logging
import os
import time

from botcity.core import DesktopBot

from config import POSTS_LIMIT, NOTEPAD_ICON_KEY, NOTEPAD_ICON_IMAGE
from utils import create_project_folder, setup_logger
from services import fetch_posts
from bot import (
    terminate_notepad,
    ground_notepad_icon,
    validate_notepad_window,
    write_post_to_notepad,
    OS_FALLBACK_SUCCESS
)


def main():

    # 1. Setup — folder must be created before logger
    project_path = create_project_folder()
    setup_logger(project_path)

    logging.info("Automation started.")

    # 2. Fetch posts from API
    # Graceful degradation: if API is unavailable, log and exit cleanly
    posts = fetch_posts()
    if not posts:
        logging.error("No posts returned from API. Aborting.")
        print("API unavailable. Check automation.log for details.")
        return

    posts = posts[:POSTS_LIMIT]
    logging.info(f"Processing {len(posts)} post(s).")

    # 3. Initialize bot
    bot = DesktopBot()
    bot.add_image(NOTEPAD_ICON_KEY, NOTEPAD_ICON_IMAGE)
    
    # 4. Process each post
    for index, post in enumerate(posts, start=1):
        logging.info(f"--- Processing post {index} of {len(posts)} ---")

        # Close any existing Notepad before starting fresh
        terminate_notepad()
        time.sleep(1)

        # Attempt to open Notepad via icon grounding
        # Returns: (x, y) if icon found, OS_FALLBACK_SUCCESS if OS launched it, None if all failed
        result = ground_notepad_icon(bot)

        if result is None:
            # True failure — both icon grounding and OS fallback failed
            logging.error("Could not open Notepad via icon or OS fallback. Aborting.")
            print("Failed to open Notepad. Check automation.log for details.")
            return

        if result == OS_FALLBACK_SUCCESS:
            # Notepad opened via OS — no coordinates, but window is confirmed open
            logging.info("Proceeding with OS-launched Notepad.")
        else:
            # Icon was found and clicked — validate window one more time
            if not validate_notepad_window():
                logging.error("Notepad window did not appear after icon click. Aborting.")
                print("Notepad window failed to open.")
                return

            x, y = result
            logging.info(f"Proceeding with icon-launched Notepad (clicked at {x}, {y}).")

        # Write post content and save to file
        file_path = os.path.join(project_path, f"post_{index}.txt")
        write_post_to_notepad(bot, post, file_path)

    # 5. Clean up
    terminate_notepad()
    logging.info("Automation completed successfully.")
    print("All files created successfully.")


if __name__ == "__main__":
    main()
