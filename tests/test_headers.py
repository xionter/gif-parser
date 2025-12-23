import tempfile
from parser.gif_parser import read_gif
from tests.gif_factory import make_gif


def test_header_1x1():
    data = make_gif(1, 1)

    with tempfile.NamedTemporaryFile(suffix=".gif") as f:
        f.write(data)
        f.flush()

        gif = read_gif(f.name)
        h = gif["header"]

        assert h["width"] == 1
        assert h["height"] == 1
        assert h["signature"] == "GIF"
