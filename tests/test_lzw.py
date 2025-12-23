from parser.utils import lzw_decode


def test_lzw_empty():
    result = lzw_decode(2, b"")
    assert result == []


def test_lzw_simple_clear_end():
    min_code_size = 2
    clear = 1 << min_code_size
    end = clear + 1

    data = bytes([clear | (end << 3)])
    result = lzw_decode(min_code_size, data)

    assert isinstance(result, list)


def test_lzw_does_not_crash_on_garbage():
    result = lzw_decode(2, b"\xff\xff\xff\xff")
    assert isinstance(result, list)
