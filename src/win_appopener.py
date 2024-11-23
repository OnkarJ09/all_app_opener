from AppOpener import open, close, mklist


def open_thing(app_name):
    """
    It will open the app specified by app_name
    :param app_name: string of the app name
    :return: None
    """
    open(app_name)
    return


def close_thing(app_name):
    """
    It will close the app specified by app_name
    :param app_name: string of the app name
    :return: None
    """
    close(app_name)
    return


def update_list_thing():
    """
    It will update the app list
    :return: app_list.json
    """
    mklist("app_list.json")



