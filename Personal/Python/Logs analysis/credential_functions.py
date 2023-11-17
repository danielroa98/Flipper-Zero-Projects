""" credential_functions.py

This module is meant to assist with the reading and filtering logs 
generated whilst using the Evil Portal with the Flipper Zero.
 """

import re
import os


def get_files(logs_path: str):
    """ get_files
    
    Function that gets all the .txt files that may contain logs.

    Receives:
        - logs_path: string containing the path to the directory containing the log files.
    Returns:
        - file_list: list of strings containing the name of each log file
    """
    file_list = [fileName for fileName in os.listdir(
        logs_path) if fileName.endswith(".txt")]
    return file_list


def cred_analysis(filepath: str) -> list:
    """ cred_analysis

    Function that cleans the contents of the log files and 
    returns the obtained usernames and passwords.

    The regex used belong specifically to the logs obtained when using
    the Evil Portal with your Flipper Zero.

    Receives:
        - logs_path: string with the path where the file is located.
    Returns:
        - username: list containing the found usernames.
        - password: list containing the found passwords.
    """
    u_reg = r"u:\s*(\S+)"
    p_reg = r"p:\s*(\S+)"
    with open(filepath, "r", encoding="utf-8") as file:
        text = file.read()
        username = re.findall(u_reg, text)
        password = re.findall(p_reg, text)
    return username, password


def gen_logs_dict(file_list: list, logs_path: str, view_logs=True) -> dict:
    """ gen_logs_dict

    Function in charge of saving the logs into a dictionary so they can be used
    in whichever way the user of this code prefers.

    Receives:
        - file_list: list containing the list of file names to be analysed.
        - logs_path: string with the path to the directory in which the files are located.
        - view_logs: boolean in charge of printing the logs to the user. Defaulted as True.

    Returns:
        - users: dictionary containing the extracted attributed from the log files.
    """
    user_list = []
    pass_list = []
    log_list = []

    for file_name in file_list:
        filepath = logs_path+file_name
        try:
            usernames, passwords = cred_analysis(filepath=filepath)

            if not usernames and not passwords:
                if view_logs:
                    print("Empty lists")
            else:
                for username in usernames:
                    user_list.append(username)
                for password in passwords:
                    pass_list.append(password)
                log_list.append(file_name)

        except Exception as exception:
            if view_logs:
                print(
                    f"There was an error reading file {file_name} at location {filepath}: \
                        {exception}"
                    )

    users = {
        "Log file": log_list,
        "Usernames": user_list,
        "Passwords": pass_list
    }

    return users
