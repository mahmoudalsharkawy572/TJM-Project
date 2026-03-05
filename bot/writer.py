import logging
import os


def write_post_to_notepad(bot, post: dict, file_path: str) -> None:
    """
    Types the post content into an open Notepad window,
    then saves it to the specified file path using Save As.

    Args:
        bot: BotCity DesktopBot instance.
        post: A dict with 'title' and 'body' keys.
        file_path: Full path where the .txt file will be saved.
    """
    # Check if file already exists before saving — determines overwrite behavior
    file_exists = os.path.exists(file_path)
    if file_exists:
        logging.info(f"File already exists, will overwrite: {file_path}")
    else:
        logging.info(f"Creating new file: {file_path}")

    text = f"Title: {post['title']}\n\n{post['body']}\n\n"

    bot.copy_to_clipboard(text=text, wait=500)
    bot.control_v(wait=500)
    logging.info(f"Pasted content for post: {post.get('title', 'Unknown')}")

    # Open Save As dialog
    bot.control_s(500)

    # Type the file path in the Save As dialog
    bot.paste(text=file_path, wait=500)
    bot.enter()

    # Only confirm overwrite dialog if file already existed
    if file_exists:
        bot.enter(500)
        logging.info("Confirmed overwrite dialog.")

    # Final save to flush
    bot.control_s(500)

    logging.info(f"File saved: {file_path}")
