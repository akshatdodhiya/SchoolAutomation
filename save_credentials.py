"""
Program to store credentials in a file
"""

import pickle

meet_usr = input("Enter your google meet's email id: ")
meet_pwd = input("Enter your google meet's password: ")
website = input("Enter your school's website url: ")
school_gr = input("Enter your id: ")
school_pwd = input("Enter your school's website's password: ")

credentials = \
    {
        'meet_usr': meet_usr,
        'meet_pwd': meet_pwd,
        'website': website,
        'school_gr': school_gr,
        'school_pw': school_pwd
    }

pickle.dump(credentials, open('credentials.pkl', 'wb'))
