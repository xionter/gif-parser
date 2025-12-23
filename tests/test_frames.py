import tempfile
from parser.gif_parser import read_gif
from tests.gif_factory import make_gif


def test_single_frame_exists():
    data = make_gif(2, 2)

    with tempfile.NamedTemporaryFile(suffix=".gif") as f:
        f.write(data)
        f.flush()

        gif = read_gif(f.name)
        assert len(gif["frames"]) == 1


def test_animation_frames():
    data = make_gif(2, 2, animated=True)

    with tempfile.NamedTemporaryFile(suffix=".gif") as f:
        f.write(data)
        f.flush()

        gif = read_gif(f.name)
        assert len(gif["frames"]) >= 2
