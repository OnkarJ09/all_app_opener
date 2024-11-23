import platform
import os


try:
    """
    Recognize the system App-Opener is running on (Windows/Linux/Mac). 
    and import the packages as needed.
    """
    if platform.system() == "Windows":
        from src.win_appopener import open_app, close_app, update_app_list
    elif platform.system() == "Linux":
        from src.linux_appopener import open_app, close_app, update_app_list
    elif platform.system() == "Darwin":
        # import logic for mac opener
        pass
    else:
        raise Exception("Unsupported OS")
except Exception as e:
    print(f"Error: {e}")


if __name__ == "__main__":
    pass



