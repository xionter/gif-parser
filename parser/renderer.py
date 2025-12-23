import os
import time
import shutil


def render_static(gif):
    render_frame(gif["frames"][0])


def render_animation(gif):
    for frame in gif["frames"]:
        os.system("cls" if os.name == "nt" else "clear")
        render_frame(frame)
        time.sleep(frame["delay"] / 100)


def render_frame(frame):
    w, h = frame["canvas"]
    term_w, term_h = shutil.get_terminal_size()

    scale_x = max(1, (w * 2) // term_w)
    scale_y = max(1, h // term_h)

    canvas = [[None]*w for _ in range(h)]

    idx = 0
    for y in range(frame["h"]):
        for x in range(frame["w"]):
            if idx >= len(frame["pixels"]):
                break
            color_idx = frame["pixels"][idx]
            idx += 1
            if frame["transparency"] is not None and color_idx == frame["transparency"]:
                continue
            if color_idx < len(frame["palette"]):
                canvas[frame["y"]+y][frame["x"]+x] = frame["palette"][color_idx]

    for y in range(0, h, scale_y):
        for x in range(0, w, scale_x):
            pixel = canvas[y][x]
            if pixel is None:
                bg = 180 if (x+y)//scale_x % 2 == 0 else 120
                print(bg_color(bg, bg, bg), end="")
            else:
                r, g, b = pixel
                print(bg_color(r, g, b), end="")
        print("\033[0m")


def bg_color(r, g, b):
    return f"\033[48;2;{r};{g};{b}m  "
