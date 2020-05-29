"""Perform search and extract counts from Google Scholar"""

import logging
import pyautogui
import pytesseract
import re

# CONFIGURE THE BELOW POSITION AND REGION VALUES
# BASED ON YOUR SETUP
# TO FIND (X, Y) COORDINATES UNDER YOUR MOUSE CURSOR
# YOU CAN USE `xdotool getmouselocation --shell` in LINUX
SEARCH_BUTTON_POSITION = (3789, 196)  # Clickable search of google scholar
TEXT_INPUT_POSITION = (3637, 184)  # Clickable input of google scholar
SCREENSHOT_REGION = (2650, 200, 400, 400)  # Must cover `Cited by <NUMBERS>`


def move_mouse_to(x: int, y: int, duration: float) -> None:
    """Moves the mouse cursor to (x, y) on your screen"""
    pyautogui.moveTo(x=x, y=y, duration=duration)


def paste_and_search(input_text: str = "") -> None:
    """Enters data and makes a search query on Google Scholar"""
    move_mouse_to(*TEXT_INPUT_POSITION, duration=0.5)
    pyautogui.click(button="left")
    pyautogui.hotkey("ctrl", "a")  # Select anything inside the input
    pyautogui.typewrite(["backspace"])  # Remove the selection
    pyautogui.typewrite(input_text)  # Enter new text
    move_mouse_to(*SEARCH_BUTTON_POSITION, duration=0.5)
    pyautogui.click(button="left")  # Click `search`


def get_citations_count_from_screen() -> int:
    """Get `Cited by` count from the screenshot"""
    im = pyautogui.screenshot(region=SCREENSHOT_REGION)
    text = pytesseract.image_to_string(im)
    try:
        citations = int(re.findall("Cited by ([0-9]+)", text)[0])
        logging.info(f"Cited {citations} times")
    except Exception as ex:
        logging.warning(f"Exception: {ex}")
        logging.warning("Citations were not found")
        citations = 0
    return citations
