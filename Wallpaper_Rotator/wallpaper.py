import ctypes
import ctypes.wintypes
import win32con
import os
import random
import time
import winreg
import json


class Wallpaper:

    registry_startup_path = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
    MAX_PATH = ctypes.wintypes.MAX_PATH

    def __init__(self, wallpaper_directory: str, interval: int, ending_time: int = None):
        self.wallpaper_directory = wallpaper_directory
        self.interval = interval
        self.random = random.SystemRandom()
        self.wallpaper_current = self.get_current_wallpaper()
        if ending_time:
            self.ending_time = ending_time
        else:
            self.ending_time = time.time() + self.interval

    def check_time(self) -> bool:
        """ Check if it's time to change the wallpaper. """
        current_time = time.time()
        if current_time >= self.ending_time:
            self.ending_time = current_time + self.interval
            return True
        return False

    def get_new_wallpaper(self) -> str:
        """ Return path to a new wallpaper from set directory. """
        all_images = os.listdir(self.wallpaper_directory)
        if len(all_images) == 1:
            return all_images[0]
        while True:
            random_index = self.random.randint(0, len(all_images) - 1)
            chosen_image = all_images[random_index]
            if chosen_image != self.wallpaper_current:
                return chosen_image

    def get_current_wallpaper(self) -> str:
        """ Get name of current wallpaper. """
        buffer = ctypes.create_unicode_buffer(self.MAX_PATH)
        ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_GETDESKWALLPAPER, len(buffer), buffer, 0)
        return os.path.basename(buffer.value)

    def set_wallpaper(self, path: str) -> None:
        """ Set image from path as wallpaper. """
        if not os.path.exists(path):
            print("Couldn't set wallpaper. Path does not exist.")
            return
        ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_SETDESKWALLPAPER, 0, path, 0)

    def check_persistence(self) -> bool:
        """ Check if program is persistent. """
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.registry_startup_path)
        try:
            t = winreg.QueryValueEx(key, "Wallpaper_Rotator")
        except Exception as e:
            print(e)
            return False
        return True

    def get_persistence(self) -> None:
        """ Persist program. """
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, self.registry_startup_path)
        try:
            winreg.SetValueEx(key, "Wallpaper_Rotator", 0, winreg.REG_SZ, f"{os.getcwd()}\\wallpaper_rotator.py")
        except Exception as e:
            print(f"Couldn't get persistence.\n{e}")
        else:
            winreg.CloseKey(key)

    def save_data(self) -> None:
        """ Write persistent data to a json file. """
        with open("data.json", "w+") as f:
            d = {"directory": self.wallpaper_directory, "interval": self.interval, "ending_time": self.ending_time}
            json.dump(d, f)

    def main_loop(self):
        """ Set new wallpaper whenever interval has passed. """
        if not self.check_persistence():
            self.get_persistence()
        while True:
            if self.check_time():
                new_wallpaper = self.get_new_wallpaper()
                new_wallpaper_path = os.path.join(self.wallpaper_directory, new_wallpaper)
                self.set_wallpaper(new_wallpaper_path)
                self.wallpaper_current = new_wallpaper
            # in case program gets interrupted
            self.save_data()
            time.sleep(self.interval)
