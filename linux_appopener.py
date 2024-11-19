import configparser
import json
import os
import subprocess
import time
from pathlib import Path

from fuzzywuzzy import process

#  ------------    APPLIST LOCATION        ------------------

PATH_APP_LIST = "list_apps.json"

#  ------------    Detect Applications     ------------------

def get_app_loc():
    """
    It will detect the app location and return it.
    :return: app location, app name
    """
    dirs = [
        Path("/usr/share/applications"),
        Path("~/.local/share/applications"),
    ]

    apps = {}

    for dir in dirs:
        if dir.exists():
            for file in dir.iterdir():
                if file.suffix == ".desktop":
                    config = configparser.ConfigParser()
                    try:
                        config.read(file)
                        name = config.get("Desktop Entry", "Name", fallback=None)
                        exec_cmd = config.get("Desktop Entry", "Exec", fallback=None)
                        if name and exec_cmd:
                            exec_cmd = exec_cmd.split(" ")[0]   # To remove unnecessary cmd from exec
                            apps[name] = exec_cmd
                    except Exception as e:
                        print(f"Error reading {file}: {e}")

    return apps


def load_apps():
    """
    It will look for the list of apps list if not exists it will create one.
    :return: list_apps.json
    """
    if Path(PATH_APP_LIST).exists():
        with open(PATH_APP_LIST, "r") as f:
            return json.load(f)
    else:
        with open(PATH_APP_LIST, "w") as f:
            apps = get_app_loc()
            save_apps(apps)
            return apps


def save_apps(apps):
    """
    It will save the list of apps.
    :param apps: str
    :return: list_apps.json
    """
    with open(PATH_APP_LIST, "w") as f:
        json.dump(apps, f, indent=4)
    print(f"Saved {len(apps)} apps to {PATH_APP_LIST}")


#  ------------     Detect Workspace      ------------------

def get_workspace():
    """
    Will get the current workspace number wmctrl.
    :return: number of workspace
    """
    try:
        output = subprocess.check_output(["wmctrl", "-d"], universal_newlines=True)
        for line in output.splitlines():
            if "*" in line:    # Current Workspace has a astric(*)
                return line.split(" ")[0]
    except subprocess.CalledProcessError:
        print("Error getting workspace")
        return 0


def get_window():
    """
    Will get a list of windows on a current workspace using wmctrl.
    :return:
    """
    try:
        output = subprocess.check_output(["wmctrl", "-l"], universal_newlines=True)
        windows = {}
        for line in output.splitlines():
            parts = line.split(None, 3)
            if len(parts) >= 4:
                win_id, workspace, _, title = parts
                windows[title.strip()] = (win_id.strip(), workspace)
        return windows
    except subprocess.CalledProcessError:
        print("Error getting windows")
        return {}


#  ------------     Opening Applications     ----------------------

def open_apps(app_name, apps):
    """
    It will open an app based on its name.
    :param app_name: str
    :param apps: str
    :return: None
    """
    match, score = process.extractOne(app_name, apps.keys())
    if score > 80:
        app_name = apps[match]
        try:
            subprocess.Popen(app_name, shell=True)
            print(f"Opening {app_name}...")

            current_window = get_window()
            for _ in range(10):
                time.sleep(1)
                new_window = get_window()
                diff = {k: v for k, v in new_window.items() if k not in current_window}
                for title, (win_id, workspace) in diff.items():
                    current_workspace = get_workspace()
                    subprocess.run(["wmctrl", "-ir", win_id, "-t", current_workspace])
                    return
        except FileNotFoundError:
            print(f"No app found with name {app_name}")
    else:
        print("No app found with name {app_name}")


#  ---------------   Close Application in Current Workspace    -------------

def get_window_in_current_workspace():
    """
    Get window id from current workspace.
    :return: window_id
    """
    try:
        current_workspace = get_workspace()
        windows = get_window()
        return {title: win_id for title, (win_id, workspace) in windows.items() if workspace == current_workspace}
    except Exception as e:
        print(f"Error getting window id: {e}")

def close_apps(app_name):
    """
    It will close an app based on its name.
    :param app_name: str
    :return: None
    """
    windows = get_window_in_current_workspace()
    if not windows:
        print("No window found in current workspace")
        return

    match, score = process.extractOne(app_name, windows.keys())
    if score > 80:
        win_id = windows[match]
        try:
            subprocess.run(["wmctrl", "-ic", win_id])
            print("Closing {app_name}...")
        except Exception as e:
            print(f"Error closing {app_name}: {e}")
    else:
        print("No app found with name {app_name}")




