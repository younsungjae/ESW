import os
from PIL import Image

# main.py가 있는 폴더 기준으로 assets/images를 찾음 (어디서 실행해도 됨)
IMAGE_DIR = os.path.join(os.path.dirname(__file__), "assets", "images")


def load(name):
    return Image.open(os.path.join(IMAGE_DIR, name + ".png")).convert("RGBA")


def draw(img, sprite, x, y):
    # (x, y)가 그림의 한가운데가 되도록 붙이기 (투명한 부분은 그대로 비침)
    left = int(x - sprite.width / 2)
    top = int(y - sprite.height / 2)
    img.paste(sprite, (left, top), sprite)


PLAYER = load("player")
BOSSES = [load("boss1"), load("boss2"), load("boss3")]
HEART = load("heart")
HEART_EMPTY = load("heart_empty")
SWORD = load("sword")
SWORD_EMPTY = load("sword_empty")
SLASH = load("slash")
ENDING1 = load("ending1")
ENDING2 = load("ending2")
