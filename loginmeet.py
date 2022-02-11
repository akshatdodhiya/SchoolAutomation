"""
Program to log in to google meet with the stored credentials
"""

from playwright.sync_api import Playwright, sync_playwright
import pickle
import os
import time
from getcolors import *

# Change directory to the directory of this script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

CREDENTIALS = pickle.load(open("credentials.pkl", "rb"))
FILENAME = "state.json"


def run(playwright: Playwright) -> None:
    """
    Login and save the state
    :param playwright: Playwright instance
    :return: None
    """
    global CREDENTIALS, FILENAME
    browser = playwright.chromium.launch(headless=False)
    try:
        context = browser.new_context(storage_state=FILENAME)

    except FileNotFoundError:
        context = browser.new_context()
        stored_state = False

    except Exception as e:
        stored_state = False
        context = browser.new_context()
        print(e)

    else:
        stored_state = True

    if not stored_state:
        # Open new page
        page = context.new_page()

        # Go to https://apps.google.com/meet/
        page.goto("https://apps.google.com/meet/")

        # Click text=Sign in with page.expect_navigation(
        with page.expect_navigation():
            page.click("text=Sign in")

        # Fill [aria-label="Email\ or\ phone"]
        page.fill("[aria-label=\"Email\\ or\\ phone\"]", CREDENTIALS['meet_usr'])

        with page.expect_navigation():
            page.press("[aria-label=\"Email\\ or\\ phone\"]", "Enter")

        # Fill [aria-label="Enter\ your\ password"]
        page.fill("[aria-label=\"Enter\\ your\\ password\"]", CREDENTIALS['meet_pwd'])

        # Press Enter
        page.press("[aria-label=\"Enter\\ your\\ password\"]", "Enter")

        time.sleep(5)

        # Save storage state into the file.
        context.storage_state(path=FILENAME)
        time.sleep(3)

        # ---------------------
    context.close()
    browser.close()


def login_meet() -> None:
    """
    Login to Google Meet
    """
    try:
        with sync_playwright() as playwright:
            run(playwright)

    except Exception as err:
        print(err)

    else:
        magenta("Logged in to google meet successfully")


if __name__ == '__main__':
    login_meet()
