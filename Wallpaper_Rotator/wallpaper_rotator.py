import argparse
import wallpaper

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", type=str, help="Directory which contains all of the wallpapers.")
    parser.add_argument("-i", "--interval", type=int, help="Change wallpaper in this interval in seconds.")
    args = parser.parse_args()
    if not (args.directory and args.interval):
        wp = wallpaper.Wallpaper()
        if d := wp.load_json():
            wp = wallpaper.Wallpaper(d["directory"], d["interval"], d["ending_time"])
            wp.main_loop()
        else:
            print("If program gets called without arguments then there needs to be a json file.")
    else:
        wp = wallpaper.Wallpaper(args.directory, args.interval)
        wp.main_loop()
