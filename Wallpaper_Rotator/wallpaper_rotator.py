import argparse
import wallpaper
import loader

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", type=str, help="Directory which contains all of the wallpapers.")
    parser.add_argument("-i", "--interval", type=int, help="Change wallpaper in this interval in seconds.")
    args = parser.parse_args()
    if not (args.directory and args.interval):
        if loader.load_json("data.json"):
            d = loader.load_json("data.json")
            wallpaper = wallpaper.Wallpaper(d["directory"], d["interval"], d["ending_time"])
            wallpaper.main_loop()
        else:
            print("If program gets called without arguments then there needs to be a json file.")
    else:
        wallpaper = wallpaper.Wallpaper(args.directory, args.interval)
        wallpaper.main_loop()
