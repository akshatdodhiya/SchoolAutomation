"""
Program to join a school meeting by clicking the link on school's website.
"""

from playwright.sync_api import Playwright, sync_playwright, TimeoutError
import pickle
import time
from getcolors import *
import os

# Change working directory to the directory of this script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

FILENAME = "state.json"
CNT = 0
CREDENTIALS = pickle.load(open("credentials.pkl", "rb"))


def login_school(context):
    """
    Login to school's website
    :param context: playwright context of currently opened browser
    :return: logged in page of school
    """
    global CREDENTIALS
    # Open new page
    page = context.new_page()

    # Go to website
    page.goto(CREDENTIALS['website'])

    try:
        # Login
        # Click [placeholder="\ "]
        page.click("[placeholder=\"\\ \"]")

        # Fill [placeholder="\ "]
        page.fill("[placeholder=\"\\ \"]", CREDENTIALS['school_gr'])

        # Click input[name="password"]
        page.click("input[name=\"password\"]")

        # Fill input[name="password"]
        page.fill("input[name=\"password\"]", CREDENTIALS['school_pw'])

        # Click button:has-text("Login")
        with page.expect_navigation():
            page.click("button:has-text(\"Login\")")

    except TimeoutError as err:
        yellow("Already logged in: ", err)

    return page


def get_context(browser):
    """
    Checks if the storage file exists.
    :return: the new context
    """
    for _ in range(2):
        try:
            context = browser.new_context(permissions=["microphone", "camera"], storage_state=FILENAME)
        except FileNotFoundError:
            red("You have not logged in to meet. Please log in.")
            exit(1)
        except Exception as e:
            if os.path.exists(FILENAME):
                os.remove(FILENAME)
            red("Error:", e)
            blue("Please log in again.")
            exit(1)
        else:
            return context


def join_meeting(playwright: Playwright):
    """
    Join the School Meeting from school's website
    :param playwright: playwright object
    :return: None
    """
    global CNT, FILENAME

    browser = playwright.chromium.launch(headless=False)
    context = get_context(browser)

    page = login_school(context)
    context.grant_permissions(["microphone", "camera"])

    # Click text=Join Now
    # Get page after a specific action (e.g. clicking a link)
    with context.expect_page() as new_page_info:
        page.click("text=Join Now")  # Opens a new tab
    page1 = new_page_info.value

    page1.wait_for_load_state()
    time.sleep(3)  # Wait for page to load

    try:
        # Click :nth-match(div[role="button"]:has-text("Dismiss"), 2)
        page1.click(":nth-match(div[role=\"button\"]:has-text(\"Dismiss\"), 2)", timeout=5000)

    except:
        pass

    try:
        # Click [aria-label="Turn\ off\ camera\ \(⌘\ \+\ e\)"]

        page1.click("[aria-label=\"Turn\\ off\\ camera\\ \\(⌘\\ \\+\\ e\\)\"]", timeout=5000)
        # # Click [aria-label="Turn\ off\ microphone\ \(⌘\ \+\ d\)"]
        page1.click("[aria-label=\"Turn\\ off\\ microphone\\ \\(⌘\\ \\+\\ d\\)\"]", timeout=5000)

    except:
        pass

    # JOIN NOW MEET
    page1.click('//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/'
                'div[3]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/span')

    # ---------------------
    context.storage_state(path=FILENAME)

    return context, browser


def join_school():
    """
    Join the School Meeting from school's website
    :return: None
    """
    with sync_playwright() as playwright:
        return join_meeting(playwright)
