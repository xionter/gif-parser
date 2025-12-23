from tests.gif_factory import make_gif

with open("example.gif", "wb") as f:
    f.write(make_gif(10, 10))

print("GIF создан: example.gif")

