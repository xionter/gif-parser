def print_header_info(h):
    print("GIF INFO")
    print(f"Signature: {h['signature']}")
    print(f"Version: {h['version']}")
    print(f"Size: {h['width']}x{h['height']}")
    print(f"Global palette: {h['global_palette_flag']}")
    if h['global_palette_flag']:
        print(f"Palette size: {h['palette_size']} colors")

def lzw_decode(min_code_size, data):
    clear_code = 1 << min_code_size
    end_code = clear_code + 1

    code_size = min_code_size + 1
    max_code_size = 12

    dictionary = {i: [i] for i in range(clear_code)}
    next_code = end_code + 1

    bit_buffer = 0
    bit_count = 0
    idx = 0

    result = []
    prev = None

    def read_code():
        nonlocal bit_buffer, bit_count, idx
        while bit_count < code_size and idx < len(data):
            bit_buffer |= data[idx] << bit_count
            bit_count += 8
            idx += 1
        if bit_count < code_size:
            return None
        code = bit_buffer & ((1 << code_size) - 1)
        bit_buffer >>= code_size
        bit_count -= code_size
        return code

    while True:
        code = read_code()
        if code is None:
            break

        if code == clear_code:
            dictionary = {i: [i] for i in range(clear_code)}
            code_size = min_code_size + 1
            next_code = end_code + 1
            prev = None
            continue

        if code == end_code:
            break

        if code in dictionary:
            entry = dictionary[code]
        elif prev is not None:
            entry = prev + [prev[0]]
        else:
            continue

        result.extend(entry)

        if prev is not None and next_code < (1 << max_code_size):
            dictionary[next_code] = prev + [entry[0]]
            next_code += 1
            if next_code >= (1 << code_size) and code_size < max_code_size:
                code_size += 1

        prev = entry

    return result

