import argparse
from parser.gif_parser import read_gif
from parser.renderer import render_animation, render_static
from parser.utils import print_header_info


def main():
    parser = argparse.ArgumentParser(description="GIF CLI parser")
    parser.add_argument("file", help="Path to gif file")
    parser.add_argument("--headers", action="store_true", help="Show GIF headers")
    parser.add_argument("--show", action="store_true", help="Show image / animation")

    args = parser.parse_args()

    gif = read_gif(args.file)

    if "error" in gif:
        print(gif["error"])
        return

    if args.headers:
        print_header_info(gif["header"])

    if args.show:
        if len(gif["frames"]) > 1:
            render_animation(gif)
        else:
            render_static(gif)


if __name__ == "__main__":
    main()
