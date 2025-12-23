import os
import pytest


def require_gif(path: str):
    if not os.path.exists(path):
        pytest.skip(f"GIF файл не найден: {path}")
