
def make_gif(width: int, height: int, animated=False) -> bytes:
    if width <= 0 or height <= 0:
        raise ValueError("Размеры GIF должны быть > 0")

    header = b"GIF89a"

    w = width.to_bytes(2, "little")
    h = height.to_bytes(2, "little")

    packed = b"\x80"
    bg_color = b"\x00"
    aspect = b"\x00"

    gct = b"\x00\x00\x00" + b"\xFF\xFF\xFF"

    gce = (
        b"\x21\xF9\x04"
        b"\x00"          
        b"\x05\x00"      
        b"\x00"
        b"\x00"
    )

    img_desc = (
        b"\x2C"
        b"\x00\x00\x00\x00"
        + w + h +
        b"\x00"
    )

    lzw_min = b"\x02"
    image_data = b"\x02\x4C\x01\x00"

    frame = img_desc + lzw_min + image_data
    trailer = b"\x3B"

    if animated:
        return (
            header + w + h + packed + bg_color + aspect + gct +
            gce + frame +
            gce + frame +
            trailer
        )

    return header + w + h + packed + bg_color + aspect + gct + frame + trailer
