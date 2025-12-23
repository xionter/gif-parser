import struct
from parser.utils import lzw_decode


def read_gif(path: str):
    try:
        with open(path, "rb") as f:
            data = f.read()
    except FileNotFoundError:
        return {"error": "Файл не найден"}

    if len(data) < 13:
        return {"error": "Файл слишком короткий"}

    header = parse_header(data)
    frames = parse_frames(data, header)

    return {
        "header": header,
        "frames": frames,
    }


def parse_header(data: bytes):
    signature = data[:3].decode()
    version = data[3:6].decode()

    width = int.from_bytes(data[6:8], "little")
    height = int.from_bytes(data[8:10], "little")

    packed = data[10]
    bg_color = data[11]

    global_palette_flag = packed & 0b10000000
    palette_size = 2 ** ((packed & 0b00000111) + 1) if global_palette_flag else 0

    return {
        "signature": signature,
        "version": version,
        "width": width,
        "height": height,
        "bg_color": bg_color,
        "global_palette_flag": bool(global_palette_flag),
        "palette_size": palette_size,
        "packed": packed,
    }


def parse_frames(data: bytes, header: dict):
    offset = 13
    frames = []

    global_palette = []

    if header["global_palette_flag"]:
        for i in range(header["palette_size"]):
            r, g, b = data[offset:offset+3]
            global_palette.append((r, g, b))
            offset += 3

    transparency = None
    delay = 10

    canvas_w = header["width"]
    canvas_h = header["height"]

    while offset < len(data):
        block = data[offset]

        if block == 0x3B:
            break

        if block == 0x21:
            label = data[offset+1]

            if label == 0xF9:
                delay = int.from_bytes(data[offset+4:offset+6], "little") or 5
                packed = data[offset+3]
                if packed & 1:
                    transparency = data[offset+6]
                offset += 8
            else:
                offset += 2
                while data[offset] != 0:
                    offset += 1 + data[offset]
                offset += 1

        elif block == 0x2C:
            x = int.from_bytes(data[offset+1:offset+3], "little")
            y = int.from_bytes(data[offset+3:offset+5], "little")
            w = int.from_bytes(data[offset+5:offset+7], "little")
            h = int.from_bytes(data[offset+7:offset+9], "little")
            packed = data[offset+9]
            offset += 10

            palette = global_palette

            if packed & 0x80:
                size = 2 ** ((packed & 0b111) + 1)
                palette = []
                for _ in range(size):
                    r, g, b = data[offset:offset+3]
                    palette.append((r, g, b))
                    offset += 3

            lzw_min = data[offset]
            offset += 1

            compressed = bytearray()
            while True:
                size = data[offset]
                offset += 1
                if size == 0:
                    break
                compressed += data[offset:offset+size]
                offset += size

            indices = lzw_decode(lzw_min, compressed)

            frames.append({
                "x": x,
                "y": y,
                "w": w,
                "h": h,
                "palette": palette,
                "pixels": indices,
                "transparency": transparency,
                "delay": delay,
                "canvas": (canvas_w, canvas_h),
            })

            transparency = None
            delay = 10

        else:
            break

    return frames
