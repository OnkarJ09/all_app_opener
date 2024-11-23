__version__ = "1.0"
__author__ = "hackdog"
import os
import platform
import re


try:
    if platform.system() == "Windows":
        from src.win_appopener import open_thing, close_thing, update_list_thing
    elif platform.system() == "Darwin":
        # import logic for mac opener
        pass
    elif platform.system() == "Linux":
        from src.linux_appopener import open_thing, close_thing, update_list_thing
    else:
        raise Exception("Unsupported OS")
except Exception as e:
    print(f"Error: {e}")


def open_app(self):
    """
    It will open the app specified by app_name replacing all other things
    :param self: query input
    :return: None
    """
    inp = self.lower()
    val=(re.compile(r'[^a-zA-Z-^0-9?,>&]').sub(" ",inp)).strip()
    if val == "":
        pass
    else:
        open_thing(inp)


def close_app(self):
    """
    It closes the app specified by app_name replacing all other things
    :param self: query input
    :return: None
    """
    inp = self.lower()
    val = (re.compile(r'[^a-zA-Z-^0-9?,>&+.]').sub(" ", inp)).strip()
    if val == "":
        pass
    else:
        close_thing(val)


def update_list():
    """
    It updates the list
    :return: app_list.json
    """
    if inp == "":
        pass
    elif "update app list" in inp:
        update_list_thing()


if __name__ == "__main__":


