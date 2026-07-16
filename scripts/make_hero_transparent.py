"""Make the near-white background of the hero image transparent.

Uses a flood fill from the image edges so that white elements *inside*
the illustration (cards, the central B platform, etc.) are preserved.
Only background pixels connected to the border are cleared.
"""
from collections import deque
from PIL import Image

SRC = "assets/barrel-image-hero.png"
DST = "assets/barrel-image-hero.png"
THRESHOLD = 34  # how far from pure white still counts as background

img = Image.open(SRC).convert("RGBA")
w, h = img.size
px = img.load()

def is_bg(x, y):
    r, g, b, a = px[x, y]
    return a > 0 and r >= 255 - THRESHOLD and g >= 255 - THRESHOLD and b >= 255 - THRESHOLD

visited = bytearray(w * h)
q = deque()

# seed the queue with every border pixel that looks like background
for x in range(w):
    for y in (0, h - 1):
        if is_bg(x, y):
            q.append((x, y))
            visited[y * w + x] = 1
for y in range(h):
    for x in (0, w - 1):
        if is_bg(x, y):
            q.append((x, y))
            visited[y * w + x] = 1

while q:
    x, y = q.popleft()
    px[x, y] = (0, 0, 0, 0)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < w and 0 <= ny < h and not visited[ny * w + nx]:
            visited[ny * w + nx] = 1
            if is_bg(nx, ny):
                q.append((nx, ny))

img.save(DST)
print(f"done: {w}x{h}, background cleared")
