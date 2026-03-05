import logging
import os
import time

import pygetwindow as gw

from bot.actions import show_desktop, open_notepad
from config import IMAGE_MATCH_THRESHOLD, MAX_GROUNDING_ATTEMPTS, NOTEPAD_WINDOW_TIMEOUT


# Sentinel value to distinguish OS fallback success from true failure
OS_FALLBACK_SUCCESS = "os_fallback"


# ----------------------------
# Validate Notepad Window
# ----------------------------
def validate_notepad_window(timeout: int = NOTEPAD_WINDOW_TIMEOUT) -> bool:
    """
    Polls for any open window whose title contains 'Notepad'.
    Returns True if found within timeout, False otherwise.
    """
    start_time = time.time()

    while time.time() - start_time < timeout:
        windows = gw.getWindowsWithTitle("Notepad")
        if windows:
            logging.info(f"Notepad window confirmed: '{windows[0].title}'")
            return True
        time.sleep(0.5)

    logging.error("Notepad window did not appear within timeout.")
    return False


# ----------------------------
# Ground Notepad Icon
# ----------------------------
def ground_notepad_icon(bot, max_attempts: int = MAX_GROUNDING_ATTEMPTS) -> tuple | str | None:
    """
    Attempts to locate the Notepad icon on the desktop via image matching.

    Returns:
        (x, y)              — icon found and Notepad opened via double-click
        OS_FALLBACK_SUCCESS — icon not found but Notepad launched via OS fallback
        None                — all attempts failed including OS fallback

    Note on multiple matching icons:
        BotCity returns the first match above the threshold. If multiple icons
        score above IMAGE_MATCH_THRESHOLD, the first one detected is used.
        Coordinates are logged so you can verify the correct icon was clicked.
    """
    for attempt in range(1, max_attempts + 1):
        logging.info(f"Grounding attempt {attempt} of {max_attempts}.")

        # Show desktop to clear any obscuring windows
        show_desktop(bot)
        bot.screenshot()

        element = bot.find("notepad_icon", matching=IMAGE_MATCH_THRESHOLD, waiting_time=2000)

        if element:
            x = bot.get_last_x()
            y = bot.get_last_y()

            # Log coordinates so reviewer can verify correct icon was detected
            logging.info(f"Notepad icon found at ({x}, {y}) on attempt {attempt}.")

            open_notepad(bot, x, y)

            # Validate Notepad window actually opened after clicking
            if validate_notepad_window():
                return x, y

            logging.warning(f"Icon clicked at ({x}, {y}) but Notepad window did not appear. "
                          f"Possible wrong icon match. Retrying...")
            terminate_notepad_if_open()
            continue

        logging.warning(f"Notepad icon not found on attempt {attempt}. Retrying...")
        time.sleep(1)

    # All grounding attempts failed — try OS fallback
    return _launch_notepad_via_os()


# ----------------------------
# OS Fallback
# ----------------------------
def _launch_notepad_via_os() -> str | None:
    """
    Launches Notepad directly via OS when icon grounding fails.

    Returns OS_FALLBACK_SUCCESS if Notepad opens, None if it also fails.
    Kept private — should only be called from ground_notepad_icon.
    """
    logging.warning("Icon not found after all attempts. Launching Notepad via OS fallback.")
    os.system("start notepad.exe")
    time.sleep(2)

    if validate_notepad_window():
        logging.info("Notepad launched successfully via OS fallback.")
        return OS_FALLBACK_SUCCESS

    logging.error("OS fallback also failed. Notepad did not open.")
    return None


# ----------------------------
# Helper: close notepad if somehow open after bad click
# ----------------------------
def terminate_notepad_if_open() -> None:
    """Closes Notepad only if it is currently open."""
    windows = gw.getWindowsWithTitle("Notepad")
    if windows:
        os.system("taskkill /IM notepad.exe /F")
        logging.info("Closed unexpected Notepad window after wrong icon detection.")
