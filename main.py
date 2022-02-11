"""
Name: School Meeting Joiner
Developer: Akshat Dodhiya ©
website: https://akshatdodhiya.tech | https://akshatdodhiya.blogspot.com
Version: 1.0
Language: Python 3.8
"""

import joinschoolmeeting
import datetime
from schedule import repeat
import schedule
from getcolors import *
import time
import json

TIME_TABLE = json.load(open('timetable.json'))


@repeat(schedule.every(5).days.until("12:00"))
def main(extra_class: dict = None):
    """
    Main function to run the program.
    :param extra_class: Get extra class if any
    :return: None
    """
    classes = get_classes(extra_class)  # Get the classes from the timetable.
    completed_classes, joined = 0, False
    period, browser = "", ""
    current_time = datetime.datetime.now().strftime("%H:%M")

    if completed_classes > len(classes.keys()) or current_time > \
            list(classes.values())[-1]:  # if completed all classes or current time is greater than last class
        # exit(0)
        pass

    for class_time in classes.values():
        if class_time == current_time and not joined:  # Join class if it is the time
            context, browser = joinschoolmeeting.join_school()  # Join the class
            green(f"Joined class {context.title} at {current_time}")
            joined = True
            period = class_time
            completed_classes += 1  # Increment completed classes

    if joined and int(period.split(":")[0]) * 60 + int(period.split(":")[1]) >= \
            int(period.split(":")[0]) * 60 + int(period.split(":")[1]) + 40:  # Check if it's already past the class
        browser.close()  # Close the browser
        joined = False  # Reset joined to false


def get_classes(extra_class) -> dict:
    """
    Get the classes from the timetable.
    :param extra_class: add the extra class to the timetable if any.
    :return: dictionary of classes.
    """
    classes = dict()
    today = datetime.datetime.today().strftime("%A")
    for day in TIME_TABLE.keys():
        if today == day:
            classes = TIME_TABLE[today]
            if extra_class:
                classes.update(extra_class)

    return classes


if __name__ == '__main__':
    printed_flag = False
    while True:
        try:
            with open("extra_class.txt", "r") as extra_classes:
                """
                Format to be written in file:
                <class_name> E.g. Physics
                <time> [with trailing zero in the beginning] ~ E.g. 08:00
                """
                extra_classes = extra_classes.read().split("\n")
                try:
                    extra_classes = {extra_classes[i]: extra_classes[i + 1] for i in range(0, len(extra_classes), 2)}
                except IndexError:
                    cyan("No extra classes")
                except Exception as e:
                    red("Error: " + str(e))
                else:
                    main(extra_classes)

                main()
        except FileNotFoundError:
            if not printed_flag:
                red("No extra class file found!")
                printed_flag = True

        except Exception as e:
            if not printed_flag:
                red("Error:", e)

        else:
            time.sleep(58)
            continue

        main()
        time.sleep(58)
