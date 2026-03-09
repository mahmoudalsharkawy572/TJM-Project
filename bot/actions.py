import logging
import os
import time
import pyautogui
pyautogui.FAILSAFE = False

from config import SHOW_DESKTOP_WAIT


def show_desktop(bot) -> None:
    """
    Minimizes all windows to expose the desktop.
    Uses an increased wait time to ensure all windows are fully minimized
    before attempting icon detection — handles slower machines.
    """
    pyautogui.hotkey("win", "d")
    time.sleep(1.5)
  


def open_notepad(bot, x: int, y: int) -> None:
    """
    Moves to the Notepad icon coordinates and double-clicks to open it.
    Coordinates must be obtained from grounding before calling this.
    """
    bot.mouse_move(x, y)
    time.sleep(1)
    bot.double_click()
    time.sleep(1)
    logging.info(f"Double-clicked Notepad icon at ({x}, {y}).")


def terminate_notepad() -> None:
    """Force-closes all running Notepad instances."""
    os.system("taskkill /IM notepad.exe /F")
    logging.info("Notepad terminated.")
